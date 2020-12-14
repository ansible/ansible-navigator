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

from . import _actions as actions
from ._runner import PlaybookRunner
from ..app import App
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
    ("(?i)^in progress$", 8),
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
    if "play name" in entry:
        if not colval:
            color = 8
        elif colname in ["% completed", "task count", "play name"]:
            failures = entry["failed"] + entry["unreachable"]
            if failures:
                color = 9
            elif entry["ok"]:
                color = 10
            else:
                color = 8
        elif colname == "changed":
            color = 11
        else:
            color = get_color(colname)

    elif "task" in entry:
        if entry["result"].lower() == "in progress":
            color = get_color(entry["result"])
        elif colname in ["result", "host", "number", "task", "task action"]:
            color = get_color(entry["result"])
        elif colname == "changed":
            if colval:
                color = 11
            else:
                color = 8
        elif colname == "duration":
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
        detail = "PLAY [{play}:{tnum}] ".format(play=obj["play"], tnum=obj["number"])
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

        if obj["changed"] is True:
            color = 11
            res = "CHANGED"
        else:
            color = next((x[1] for x in RESULT_TO_COLOR if re.match(x[0], obj["result"])), 0)
            res = obj["result"]

        if "res" in obj and "msg" in obj["res"]:
            msg = str(obj["res"]["msg"]).replace("\n", " ").replace("\r", "")
        else:
            msg = ""

        string = "{res}: [{host}] {msg}".format(res=res, host=obj["host"], msg=msg)
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
    "play name",
    "ok",
    "changed",
    "unreachable",
    "failed",
    "skipped",
    "ignored",
    "in progress",
    "task count",
    "% completed",
]

TASK_LIST_COLUMNS = [
    "result",
    "host",
    "number",
    "changed",
    "task",
    "task action",
    "duration",
]


@actions.register
class Action(App):

    # pylint: disable=too-many-instance-attributes
    """:explore"""

    KEGEX = r"^e(?:xplore)?(\s(?P<playbook>\S+))?(\s(?P<params>.*))?$"

    def __init__(self):
        super().__init__()
        self._name = "explore"
        self.name = f"{self._name}_{str(uuid.uuid4())}"
        self.args: Namespace
        self._interaction: Interaction
        self._calling_app: App
        self._logger = logging.getLogger()
        self._parser_error: str

        self._msg_from_plays = (None, None)
        self._queue = Queue()
        self.runner = None
        self._runner_finished = None
        self._auto_scroll = False

        self._plays = Step(
            name="plays",
            tipe="menu",
            columns=PLAY_COLUMNS,
            value=[],
            show_func=self._play_stats,
            select_func=self._task_list_for_play,
        )

    def parser_error(self, message):
        """callback for parser error"""
        self._parser_error = message
        return None, None

    def playbook(self, args: Namespace) -> None:
        """Run in oldschool mode, just stdout"""
        self.args = args
        self._run_runner()
        while True:
            self._dequeue()
            if self.runner.finished:
                if self.args.artifact:
                    self.write_artifact(self.args.artifact)
                self._logger.debug("runner finished")
                break

    def run(self, interaction: Interaction, app) -> None:
        # pylint: disable=too-many-branches
        """Handle :inventory

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("explorer requested")
        self._calling_app = app
        self._interaction = interaction

        playbook = interaction.action.match.groupdict().get("playbook")
        params = interaction.action.match.groupdict().get("params")
        if playbook:
            playbook = os.path.abspath(playbook)
            if params:
                self._logger.debug(
                    "Parsing full cli command: %s %s %s", self._name, playbook, params
                )
                params = [self._name] + [playbook] + params.split()
                new_args = self._update_args(params)
                if new_args:
                    self.args = new_args
                else:
                    return None
            else:
                self.args = copy.copy(self._calling_app.args)
                self.args.playbook = playbook
                self._logger.debug(
                    "Using original cli commands with updated playbook: %s", playbook
                )
        else:
            self._logger.debug("Using original cli commands")
            self.args = self._calling_app.args

        self._run_runner()
        self.steps.append(self._plays)

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)

        while True:
            self._calling_app.update()
            self.update()

            self._take_step()

            if self.steps.current.name == "quit":
                if self.args.app == "load":
                    return self.steps.current
                done = self._prepare_to_quit(self.steps.current)
                if done:
                    return self.steps.current
                self.steps.back_one()

            if not self.steps:
                if self._calling_app.args.app == self.name:
                    self.steps.append(self._plays)
                elif not self._runner_finished:
                    self._logger.error("Can not step back while playbook in progress, :q! to exit")
                    self.steps.append(self._plays)
                else:
                    break

        interaction.ui.scroll(previous_scroll)
        return None

    def _take_step(self) -> None:
        if isinstance(self.steps.current, Interaction):
            result = self.actions.run(
                action=self.steps.current.name,
                app=self,
                interaction=self.steps.current,
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
        self._logger.debug("Starting playbook run request")
        self.runner = PlaybookRunner(args=self.args, queue=self._queue)
        self.runner.run()
        self._runner_finished = False
        self._logger.debug("Completed playbook run request")

    def _dequeue(self) -> None:
        """Drain the runner queue"""
        drain_count = 0
        while not self._queue.empty():
            message = self._queue.get()
            self._handle_message(message)
            drain_count += 1
        if drain_count:
            self._logger.debug("Drained %s ansible-runner events", drain_count)

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
            play["play name"] = play["name"]
            del play["name"]
            play["tasks"] = []
            self._plays.value.append(play)

        if event.startswith("runner_on_"):
            runner_event = event.split("_")[2]
            task = message["event_data"]
            task["task action"] = task["task_action"]
            del task["task_action"]
            play_id = next(
                idx for idx, p in enumerate(self._plays.value) if p["uuid"] == task["play_uuid"]
            )
            if runner_event in ["ok", "skipped", "unreachable", "failed"]:
                if runner_event == "failed" and task["ignore_errors"]:
                    result = "ignored"
                else:
                    result = runner_event
                task["result"] = result.upper()
                task["changed"] = task.get("res", {}).get("changed", False)
                task["_duration"] = task["duration"]
                task["duration"] = human_time(seconds=round(task["duration"], 2))
                for idx, play_task in enumerate(self._plays.value[play_id]["tasks"]):
                    if task["task_uuid"] == play_task["task_uuid"]:
                        if task["host"] == play_task["host"]:
                            task_id = idx
                            break
                self._plays.value[play_id]["tasks"][task_id].update(task)

            elif runner_event == "start":
                task["result"] = "IN PROGRESS"
                task["changed"] = "unknown"
                task["duration"] = None
                task["number"] = len(self._plays.value[play_id]["tasks"])
                self._plays.value[play_id]["tasks"].append(task)

    def _play_stats(self) -> None:
        """Calculate the play's stats based
        on it's tasks
        """
        for idx, play in enumerate(self._plays.value):
            total = ["ok", "skipped", "failed", "unreachable", "ignored", "in progress"]
            self._plays.value[idx].update(
                {
                    tot: len([t for t in play["tasks"] if t["result"].lower() == tot])
                    for tot in total
                }
            )
            self._plays.value[idx]["changed"] = len(
                [t for t in play["tasks"] if t["changed"] is True]
            )
            task_count = len(play["tasks"])
            self._plays.value[idx]["task count"] = task_count
            completed = task_count - self._plays.value[idx]["in progress"]
            if completed:
                new = round((completed / task_count * 100))
                current = self._plays.value[idx].get("_pcomplete", 0)
                self._plays.value[idx]["_pcomplete"] = max(new, current)
                self._plays.value[idx]["% completed"] = str(max(new, current)) + "%"
            else:
                self._plays.value[idx]["% completed"] = "0%"

    def _prepare_to_quit(self, interaction: Interaction) -> Union[bool, None]:
        """Looks like we're headed out of here

        :param result: the result from the ui
        :type result: dict
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
            return None
        self._logger.debug("runner not running")
        return True

    def _task_list_for_play(self) -> Step:
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
        value = self.steps.current.value
        index = self.steps.current.index
        step = Step(name="task", tipe="content", index=index, value=value)
        return step

    def update(self) -> None:
        """Drain the queue, set the status and write the artifact if needed"""
        if self.runner:
            self._dequeue()
            self._set_status()

            if self.runner.finished and not self._runner_finished:
                # self._interaction.ui.disable_refresh()
                self._logger.debug("runner finished")
                if hasattr(self.args, "artifact"):
                    self.write_artifact(self.args.artifact)
                self._runner_finished = True

    def _get_status(self) -> Tuple[str, int]:
        """Get the status and color"""
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
                "plays": self._plays.value,
                "stdout": self.stdout,
                "status": status,
                "status_color": status_color,
            }
            json.dump(artifact, outfile, indent=4)
        self._logger.info("Saved artifact as %s", filename)
