""" :explore
"""
import copy
import curses
import json
import logging
import os
import re
import uuid

from argparse import Namespace
from queue import Queue
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union


from . import run as run_action
from . import _actions as actions

from ._runner import PlaybookRunner
from ..app import App
from ..app_public import AppPublic
from ..curses_defs import CursesLinePart
from ..curses_defs import CursesLines
from ..steps import Step
from ..ui import Interaction
from ..utils import check_for_ansible
from ..utils import human_time
from ..utils import set_ansible_envar


RESULT_TO_COLOR = [
    ("(?i)^failed$", 9),
    ("(?i)^ok$", 10),
    ("(?i)^ignored$", 13),
    ("(?i)^skipped$", 14),
    ("(?i)^in_progress$", 8),
]

get_color = lambda word: next((x[1] for x in RESULT_TO_COLOR if re.match(x[0], word)), 0)


def color_menu(_colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=too-many-branches
    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """

    colval = entry[colname]
    color = 0
    if "__play_name" in entry:
        if not colval:
            color = 8
        elif colname in ["__% completed", "__task_count", "__play_name"]:
            failures = entry["__failed"] + entry["__unreachable"]
            if failures:
                color = 9
            elif entry["__ok"]:
                color = 10
            else:
                color = 8
        elif colname == "__changed":
            color = 11
        else:
            color = get_color(colname[2:])

    elif "task" in entry:
        if entry["__result"].lower() == "__in_progress":
            color = get_color(entry["__result"])
        elif colname in ["__result", "__host", "__number", "__task", "__task_action"]:
            color = get_color(entry["__result"])
        elif colname == "__changed":
            if colval is True:
                color = 11
            else:
                color = get_color(entry["__result"])
        elif colname == "__duration":
            color = 12

    return color


def content_heading(obj: Any, screen_w: int) -> Union[CursesLines, None]:
    """create a heading for some piece fo content showing

    :param obj: The content going to be shown
    :type obj: Any
    :param screen_w: The current screen width
    :type screen_w: int
    :return: The heading
    :rtype: Union[CursesLines, None]
    """

    if isinstance(obj, dict) and "task" in obj:
        heading = []
        detail = "PLAY [{play}:{tnum}] ".format(play=obj["play"], tnum=obj["__number"])
        stars = "*" * (screen_w - len(detail))
        heading.append(
            tuple(
                [
                    CursesLinePart(
                        column=0,
                        string=detail + stars,
                        color=curses.color_pair(0),
                        decoration=0,
                    )
                ]
            )
        )

        detail = "TASK [{task}] ".format(task=obj["task"])
        stars = "*" * (screen_w - len(detail))
        heading.append(
            tuple(
                [
                    CursesLinePart(
                        column=0,
                        string=detail + stars,
                        color=curses.color_pair(0),
                        decoration=0,
                    )
                ]
            )
        )

        if obj["__changed"] is True:
            color = 11
            res = "CHANGED"
        else:
            color = next((x[1] for x in RESULT_TO_COLOR if re.match(x[0], obj["__result"])), 0)
            res = obj["__result"]

        if "res" in obj and "msg" in obj["res"]:
            msg = str(obj["res"]["msg"]).replace("\n", " ").replace("\r", "")
        else:
            msg = ""

        string = "{res}: [{host}] {msg}".format(res=res, host=obj["__host"], msg=msg)
        string = string + (" " * (screen_w - len(string) + 1))
        heading.append(
            tuple(
                [
                    CursesLinePart(
                        column=0,
                        string=string,
                        color=curses.color_pair(color),
                        decoration=curses.A_UNDERLINE,
                    )
                ]
            )
        )
        return tuple(heading)
    return None


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    return {k: v for k, v in obj.items() if not (k.startswith("_") or k.endswith("uuid"))}


PLAY_COLUMNS = [
    "__play_name",
    "__ok",
    "__changed",
    "__unreachable",
    "__failed",
    "__skipped",
    "__ignored",
    "__in_progress",
    "__task_count",
    "__% completed",
]

TASK_LIST_COLUMNS = [
    "__result",
    "__host",
    "__number",
    "__changed",
    "__task",
    "__task_action",
    "__duration",
]


@actions.register
class Action(App):

    # pylint: disable=too-many-instance-attributes
    """:explore"""

    KEGEX = r"""
            (?x)
            ^
            (?P<explore>e(?:xplore)?
            (\s(?P<playbook>\S+))?
            (\s(?P<params>.*))?)
            |
            (?P<load>l(?:oad)?
            \s(?P<artifact>\S+))
            $"""

    def __init__(self, args):
        # for display purposes use the 4: of the uuid
        super().__init__(args=args)
        self._name_at_cli = "explore"
        self._uuid = str(uuid.uuid4())
        self.name = self._name_at_cli + self._uuid[-4:]
        self._logger = logging.getLogger(f"{__name__}.{self._uuid[-4:]}")

        self.args: Namespace
        self._interaction: Interaction
        self._calling_app: AppPublic
        self._parser_error: str
        self._subaction_type: str

        self._msg_from_plays = (None, None)
        self._queue = Queue()
        self.runner = None
        self._runner_finished: bool
        self._auto_scroll = False

        self._plays = Step(
            name="plays",
            tipe="menu",
            columns=PLAY_COLUMNS,
            value=[],
            show_func=self._play_stats,
            select_func=self._task_list_for_play,
        )

    def parser_error(self, message: str) -> Tuple[None, None]:
        """callback for parser error

        :param message: A message from the parser
        :type message: str
        """
        self._parser_error = message
        return None, None

    def playbook(self) -> None:
        """Run in oldschool mode, just stdout

        :param args: The parsed args from the cli
        :type args: Namespace
        """
        self._subaction_type = "playbook"
        self._logger.debug("subaction type is %s", self._subaction_type)
        self._run_runner()
        while True:
            self._dequeue()
            if self.runner.finished:
                if self.args.artifact:
                    self.write_artifact(self.args.artifact)
                self._logger.debug("runner finished")
                break

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        # pylint: disable=too-many-branches
        """run :explore or :load

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """

        self._calling_app = app
        self._interaction = interaction

        if interaction.action.match.groupdict()["explore"]:
            self._subaction_type = "explore"
            self._logger.debug("subaction type is %s", self._subaction_type)
            initialized = self._init_explore()
        elif interaction.action.match.groupdict()["load"]:
            self._subaction_type = "load"
            self._logger.debug("subaction type is %s", self._subaction_type)
            artifact_file = os.path.abspath(interaction.action.match.groupdict()["artifact"])
            initialized = self._init_load(artifact_file)
        else:
            return None

        if not initialized:
            return None

        # update the args to a unique name
        # this ensures no collision between
        # this instance and the original cli call
        self.args.app = self._uuid

        self.steps.append(self._plays)
        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)

        while True:
            self.update()

            self._take_step()

            if not self.steps:
                # if we came from the cli
                if self._calling_app.args.app in ("explore", "load"):
                    self._logger.debug("called from cli addining original step to stack")
                    self.steps.append(self._plays)
                elif not self._runner_finished:
                    self._logger.error("Can not step back while playbook in progress, :q! to exit")
                    self.steps.append(self._plays)
                else:
                    self._logger.debug(
                        "no steps remaining for %s returning to calling app", self.name
                    )
                    break

            if self.steps.current.name == "quit":
                if self.args.app == "load":
                    return self.steps.current
                done = self._prepare_to_quit(self.steps.current)
                if done:
                    return self.steps.current
                self.steps.back_one()

        interaction.ui.scroll(previous_scroll)
        return None

    def _init_explore(self) -> bool:
        """in the case of :explore, parse the user input

        0) if no playbook or params, use the original cli args
        1) if just a playbook was provided, use the cli args and the playbook
        2) if other params were provided, use those entirely
        """

        playbook = self._interaction.action.match.groupdict().get("playbook")
        params = self._interaction.action.match.groupdict().get("params")
        if playbook:
            playbook = os.path.abspath(playbook)
            if params:
                self._logger.debug(
                    "Parsing full cli command: %s %s %s", self._name_at_cli, playbook, params
                )
                params = [self._name_at_cli] + [playbook] + params.split()
                new_args = self._update_args(params)
                if new_args:
                    self.args = new_args
                else:
                    return False
            else:
                self.args = copy.copy(self._calling_app.args)
                self.args.playbook = playbook
                self._logger.debug(
                    "Using original cli commands with updated playbook: %s", playbook
                )
        else:
            self._logger.debug("Using original cli commands")
            self.args = copy.copy(self._calling_app.args)
        self._run_runner()
        self._logger.info("Explore initialized and playbook started.")
        return True

    def _init_load(self, artifact_file: str) -> bool:
        """in the case of :load, load the artifact
        check for a version, to be safe
        copy the calling app args as our our so the can be updated safely
        with a uuid attached to the name
        """
        self._logger.debug("Starting load artifact request")

        try:
            with open(artifact_file) as json_file:
                data = json.load(json_file)
        except json.JSONDecodeError as exc:
            self._logger.debug("json decode error: %s", str(exc))
            self._logger.debug("tried: %s", data)
            self._logger.error("Unable to parse artifact file")
            return False

        if (version := data.get("version", "")).startswith("1."):
            try:
                self._plays.value = data["plays"]
                self._interaction.ui.update_status(data["status"], data["status_color"])
                self.stdout = data["stdout"]
            except KeyError as exc:
                self._logger.debug("missing keys from artifact file")
                self._logger.debug("error was: %s", str(exc))
                return False
        else:
            self._logger.error(
                "Incompatible artifact version, got '%s', compatible = '1.y.z'", version
            )
            return False

        self.args = copy.copy(self._calling_app.args)
        self._runner_finished = True
        self._logger.debug("Completed load artifact request")
        return True

    def _take_step(self) -> None:
        """run the current step on the stack"""
        if isinstance(self.steps.current, Interaction):
            result = run_action(
                self.steps.current.name,
                self.app,
                self.steps.current,
            )
        elif isinstance(self.steps.current, Step):
            if self.steps.current.show_func:
                self.steps.current.show_func()

            if self.steps.current.type == "menu":

                new_scroll = len(self.steps.current.value)
                if self._auto_scroll:
                    self._interaction.ui.scroll(new_scroll)

                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=color_menu,
                )

                if self._interaction.ui.scroll() < new_scroll and self._auto_scroll:
                    self._logger.debug("autoscroll disabled")
                    self._auto_scroll = False
                elif self._interaction.ui.scroll() >= new_scroll and not self._auto_scroll:
                    self._logger.debug("autoscroll enabled")
                    self._auto_scroll = True

            elif self.steps.current.type == "content":
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    index=self.steps.current.index,
                    content_heading=content_heading,
                    filter_content_keys=filter_content_keys,
                )
        if result is None:
            self.steps.back_one()
        else:
            self.steps.append(result)

    def _update_args(self, params: List) -> Union[Namespace, None]:
        """pass the param through the original cli parser
        as if explore was run from the command line
        provide an error callback so the app doesn't sys.exit if the aprsing fails
        """

        try:
            msgs, new_args = self._calling_app.args.parse_and_update(
                params=params, error_cb=self.parser_error
            )
        except TypeError:
            self._logger.error("While attempting to parse %s:", " ".join(params))
            self._logger.error(self._parser_error)
            return None

        for msg in msgs:
            self._logger.debug(msg)

        args = copy.copy(self._calling_app.args)
        for key, value in vars(new_args).items():
            if (arg_value := getattr(args, key, None)) != value:
                self._logger.debug(
                    "Overriding previous cli param '%s:%s' with '%s:%s'", key, arg_value, key, value
                )
                setattr(args, key, value)

        if not hasattr(args, "requires_ansible") or args.requires_ansible:
            if not args.execution_environment:
                success, msg = check_for_ansible()
                if success:
                    self._logger.debug(msg)
                else:
                    self._logger.critical(msg)
                    return None
            set_ansible_envar()

        if not hasattr(args, "playbook"):
            self._logger.error(
                "No playbook specified or previous provided when starting application"
            )
            return None

        return args

    def _run_runner(self) -> None:
        """ spin up runner """
        self.runner = PlaybookRunner(args=self.args, queue=self._queue)
        self.runner.run()
        self._runner_finished = False
        self._logger.debug("runner requested to start")

    def _dequeue(self) -> None:
        """Drain the runner queue"""
        drain_count = 0
        while not self._queue.empty():
            message = self._queue.get()
            self._handle_message(message)
            drain_count += 1
        if drain_count:
            self._logger.debug("Drained %s events", drain_count)

    def _handle_message(self, message: dict) -> None:
        # pylint: disable=too-many-branches
        """Handle a runner message

        :param message: The message from runner
        :type message: dict
        """
        event = message["event"]

        if "stdout" in message and message["stdout"]:
            self.stdout.extend(message["stdout"].splitlines())
            if self.args.app == "playbook":
                print(message["stdout"])

        if event in ["verbose", "error"]:
            if "ERROR!" in message["stdout"]:
                self._msg_from_plays = ("ERROR", 9)
            elif "WARNING" in message["stdout"]:
                self._msg_from_plays = ("WARNINGS", 13)

        if event == "playbook_on_play_start":
            play = message["event_data"]
            play["__play_name"] = play["name"]
            play["tasks"] = []
            self._plays.value.append(play)

        if event.startswith("runner_on_"):
            runner_event = event.split("_")[2]
            task = message["event_data"]
            play_id = next(
                idx for idx, p in enumerate(self._plays.value) if p["uuid"] == task["play_uuid"]
            )
            if runner_event in ["ok", "skipped", "unreachable", "failed"]:
                if runner_event == "failed" and task["ignore_errors"]:
                    result = "ignored"
                else:
                    result = runner_event
                task["__result"] = result.upper()
                task["__changed"] = task.get("res", {}).get("changed", False)
                task["__duration"] = human_time(seconds=round(task["duration"], 2))
                for idx, play_task in enumerate(self._plays.value[play_id]["tasks"]):
                    if task["task_uuid"] == play_task["task_uuid"]:
                        if task["host"] == play_task["host"]:
                            task_id = idx
                            break
                self._plays.value[play_id]["tasks"][task_id].update(task)

            elif runner_event == "start":
                task["__host"] = task["host"]
                task["__result"] = "IN_PROGRESS"
                task["__changed"] = "unknown"
                task["__duration"] = None
                task["__number"] = len(self._plays.value[play_id]["tasks"])
                task["__task"] = task["task"]
                task["__task_action"] = task["task_action"]
                self._plays.value[play_id]["tasks"].append(task)

    def _play_stats(self) -> None:
        """Calculate the play's stats based
        on it's tasks
        """
        for idx, play in enumerate(self._plays.value):
            total = ["__ok", "__skipped", "__failed", "__unreachable", "__ignored", "__in_progress"]
            self._plays.value[idx].update(
                {
                    tot: len([t for t in play["tasks"] if t["__result"].lower() == tot[2:]])
                    for tot in total
                }
            )
            self._plays.value[idx]["__changed"] = len(
                [t for t in play["tasks"] if t["__changed"] is True]
            )
            task_count = len(play["tasks"])
            self._plays.value[idx]["__task_count"] = task_count
            completed = task_count - self._plays.value[idx]["__in_progress"]
            if completed:
                new = round((completed / task_count * 100))
                current = self._plays.value[idx].get("__pcomplete", 0)
                self._plays.value[idx]["__pcomplete"] = max(new, current)
                self._plays.value[idx]["__% completed"] = str(max(new, current)) + "%"
            else:
                self._plays.value[idx]["__% completed"] = "0%"

    def _prepare_to_quit(self, interaction: Interaction) -> bool:
        """Looks like we're headed out of here

        :param interaction: the quit interaction
        :type interaction: Interaction
        :return: a bool indicating whether of not it's safe to exit
        :rtype: bool
        """
        self.update()
        if not self.runner.finished:
            if interaction.action.match.groupdict()["exclamation"]:
                self._logger.debug("shutting down runner")
                self.runner.cancelled = True
                while not self.runner.finished:
                    pass
                if hasattr(self.args, "artifact"):
                    self.write_artifact(self.args.artifact)
                return True
            self._logger.warning("Quit requested but playbook running, try q! or quit!")
            return False
        self._logger.debug("runner not running")
        return True

    def _task_list_for_play(self) -> Step:
        """generate a menu of task for the currently selected play

        :return: The menu step
        :rtype: Step
        """
        value = self.steps.current.selected["tasks"]
        step = Step(
            name="task_list",
            tipe="menu",
            columns=TASK_LIST_COLUMNS,
            select_func=self._task_from_task_list,
            value=value,
        )
        return step

    def _task_from_task_list(self) -> Step:
        """generate task content for the selected task

        :return: content whic show a task
        :rtype: Step
        """
        value = self.steps.current.value
        index = self.steps.current.index
        step = Step(name="task", tipe="content", index=index, value=value)
        return step

    def update(self) -> None:
        """Drain the queue, set the status and write the artifact if needed"""

        # let the calling app update as well
        self._calling_app.update()

        if self.runner:
            self._dequeue()
            self._set_status()

            if self.runner.finished and not self._runner_finished:
                # self._interaction.ui.disable_refresh()
                self._logger.debug("runner finished")
                self._logger.info("Playbook complete")
                if hasattr(self.args, "artifact"):
                    self.write_artifact(self.args.artifact)
                self._runner_finished = True

    def _get_status(self) -> Tuple[str, int]:
        """Get the status and color

        :return: status string, status color
        :rtype: tuple of str and int
        """
        if self.runner and self.runner.finished:
            status = self.runner.status
            if self.runner.status == "failed":
                status_color = 9
            else:
                status_color = self._msg_from_plays[1] or 10
        else:
            if self._msg_from_plays[0]:
                status = self._msg_from_plays[0]
                status_color = self._msg_from_plays[1]
            else:
                status = self.runner.status
                status_color = 10
        return status, status_color

    def _set_status(self) -> None:
        """ Set the ui status """
        status, status_color = self._get_status()
        self._interaction.ui.update_status(status, status_color)

    def write_artifact(self, filename: str) -> None:
        """Write the artifact

        :param filename: The file to write to
        :type filename: str
        """
        status, status_color = self._get_status()
        with open(filename, "w") as outfile:
            artifact = {
                "version": "1.0.0",
                "plays": self._plays.value,
                "stdout": self.stdout,
                "status": status,
                "status_color": status_color,
            }
            json.dump(artifact, outfile, indent=4)
        self._logger.info("Saved artifact as %s", filename)

    def rerun(self) -> None:
        """rerun the current playbook
        since we're not reinstantiating explore,
        drain the queue, clear the steps, reset the index, etc
        """
        if self.runner.finished:
            if self._subaction_type == "explore":
                self._plays.value = []
                self._plays.index = None
                self._msg_from_plays = (None, None)
                self._queue.queue.clear()
                self.stdout = []
                self._run_runner()
                self.steps.clear()
                self.steps.append(self._plays)
                self._logger.debug("Playbook rerun triggered")
                return
            self._logger.error("No rerun available when artifact is loaded")
            return
        self._logger.warning("Playbook rerun ignored, current playbook not complete")
        return
