""" :run
"""
import curses
import datetime
import json
import logging
import os
import re
import shlex
import shutil
import uuid

from math import floor
from queue import Queue
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from . import run_action
from . import _actions as actions

from ..runner.api import CommandRunnerAsync
from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..steps import Step
from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import dict_to_form
from ..ui_framework import form_to_dict
from ..ui_framework import warning_notification


from ..utils import abs_user_path
from ..utils import human_time
from ..utils import remove_ansi


RESULT_TO_COLOR = [
    ("(?i)^failed$", 9),
    ("(?i)^ok$", 10),
    ("(?i)^ignored$", 13),
    ("(?i)^skipped$", 14),
    ("(?i)^in_progress$", 8),
]

get_color = lambda word: next(  # noqa: E731
    (x[1] for x in RESULT_TO_COLOR if re.match(x[0], word)), 0
)


def color_menu(_colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    # pylint: disable=too-many-branches
    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """

    colval = entry[colname]
    color = 0
    decoration = 0
    if "__play_name" in entry:
        if not colval:
            color = 8
        elif colname in ["__task_count", "__play_name", "__progress"]:
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

        if colname == "__progress" and entry["__progress"].strip().lower() == "complete":
            decoration = curses.A_BOLD

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

    return color, decoration


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
            tuple([CursesLinePart(column=0, string=detail + stars, color=0, decoration=0)])
        )

        detail = "TASK [{task}] ".format(task=obj["task"])
        stars = "*" * (screen_w - len(detail))
        heading.append(
            tuple([CursesLinePart(column=0, string=detail + stars, color=0, decoration=0)])
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
                        color=color,
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
    "__progress",
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
    """:run"""

    KEGEX = r"""(?x)
            ^
            (?P<run>r(?:un)?
            (\s(?P<params_run>.*))?)
            $"""

    def __init__(
        self,
        args: ApplicationConfiguration,
        play_columns: List = PLAY_COLUMNS,
        task_list_columns: List = TASK_LIST_COLUMNS,
        content_key_filter: Callable = filter_content_keys,
    ):
        # pylint: disable=dangerous-default-value
        # for display purposes use the 4: of the uuid
        super().__init__(args=args, logger_name=__name__, name="run")

        self._subaction_type: str
        self._msg_from_plays: Tuple[Optional[str], Optional[int]] = (None, None)
        self._queue: Queue = Queue()
        self.runner: CommandRunnerAsync
        self._runner_finished: bool
        self._auto_scroll = False

        self._plays = Step(
            name="plays",
            tipe="menu",
            columns=play_columns,
            value=[],
            show_func=self._play_stats,
            select_func=self._task_list_for_play,
        )
        self._task_list_columns = task_list_columns
        self._content_key_filter = content_key_filter

    @property
    def mode(self):
        """if mode == stdout and playbook artifact creation is enabled
        run in interactive mode, but print stdout"""
        if all(
            (
                self._args.mode == "stdout",
                self._args.playbook_artifact_enable,
                self._args.app != "replay",
            )
        ):
            return "stdout_w_artifact"
        return self._args.mode

    def run_stdout(self) -> int:
        """Run in oldschool mode, just stdout

        :param args: The parsed args from the cli
        :type args: Namespace
        """
        if self._args.app == "replay":
            successful: bool = self._init_replay()
            return 0 if successful else 1

        self._logger.debug("playbook requested in interactive mode")
        self._subaction_type = "playbook"
        self._logger = logging.getLogger(f"{__name__}_{self._subaction_type}")
        self._run_runner()
        while True:
            self._dequeue()
            if self.runner.finished:
                if self._args.playbook_artifact_enable:
                    self.write_artifact()
                self._logger.debug("runner finished")
                break
        return self.runner.ansible_runner_instance.rc

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """run :run or :replay

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """

        self._prepare_to_run(app, interaction)

        if interaction.action.match.groupdict().get("run"):
            self._logger.debug("run requested in interactive mode")
            self._subaction_type = "run"
            str_uuid = str(uuid.uuid4())
            self._logger = logging.getLogger(f"{__name__}_{str_uuid[-4:]}")
            self._name = f"run_{str_uuid[-4:]}"
            initialized = self._init_run()
        elif interaction.action.match.groupdict().get("replay"):
            self._logger.debug("replay requested in interactive mode")
            self._subaction_type = "replay"
            self._name = "replay"
            self._logger = logging.getLogger(f"{__name__}_{self._subaction_type}")
            initialized = self._init_replay()

        if not initialized:
            self._prepare_to_exit(interaction)
            return None

        self.steps.append(self._plays)

        while True:
            self.update()

            self._take_step()

            if not self.steps:
                if not self._runner_finished:
                    self._logger.error("Can not step back while playbook in progress, :q! to exit")
                    self.steps.append(self._plays)
                else:
                    self._logger.debug(
                        "No steps remaining for '%s' returning to calling app", self._name
                    )
                    break

            if self.steps.current.name == "quit":
                if self._args.app == "replay":
                    self._prepare_to_exit(interaction)
                    return self.steps.current
                done = self._prepare_to_quit(self.steps.current)
                if done:
                    self._prepare_to_exit(interaction)
                    return self.steps.current
                self.steps.back_one()

        self._prepare_to_exit(interaction)
        return None

    # pylint: disable=too-many-branches
    def _init_run(self) -> bool:
        """in the case of :run, check the user input"""

        # Ensure the playbook and inventory are valid

        self._update_args(
            ["run"] + shlex.split(self._interaction.action.match.groupdict()["params_run"] or "")
        )

        if isinstance(self._args.playbook, str):
            playbook_valid = os.path.exists(self._args.playbook)
        else:
            playbook_valid = False

        if isinstance(self._args.inventory, list):
            inventory_valid = all((os.path.exists(inv) for inv in self._args.inventory))
        else:
            # Permit running without an inventory
            inventory_valid = True

        if not all((playbook_valid, inventory_valid)):

            populated_form = self._prompt_for_playbook()
            if populated_form["cancelled"]:
                return False

            new_cmd = ["run"]
            new_cmd.append(populated_form["fields"]["playbook"]["value"])
            for field in populated_form["fields"].values():
                if field["name"].startswith("inv_") and field["value"] != "":
                    new_cmd.extend(["-i", field["value"]])
            if populated_form["fields"]["cmdline"]["value"]:
                new_cmd.extend(shlex.split(populated_form["fields"]["cmdline"]["value"]))

            # Parse as if provided from the cmdline
            self._update_args(new_cmd)

        self._run_runner()
        self._logger.info("Run initialized and playbook started.")
        return True

    def _init_replay(self) -> bool:
        """in the case of :replay, replay the artifact
        check for a version, to be safe
        copy the calling app args as our our so the can be updated safely
        with a uuid attached to the name
        """
        self._logger.debug("Starting replay artifact request with mode %s", self.mode)

        if self.mode == "interactive":
            self._update_args(
                ["replay"]
                + shlex.split(self._interaction.action.match.groupdict()["params_replay"] or "")
            )

        artifact_file = self._args.playbook_artifact_replay

        if isinstance(self._args.playbook_artifact_replay, str):
            artifact_valid = os.path.exists(self._args.playbook_artifact_replay)
        else:
            artifact_valid = False

        if not artifact_valid and self.mode == "interactive":
            populated_form = self._prompt_for_artifact(artifact_file=artifact_file)
            if populated_form["cancelled"]:
                return False
            artifact_file = populated_form["fields"]["artifact_file"]["value"]

        try:
            with open(artifact_file) as json_file:
                data = json.load(json_file)
        except json.JSONDecodeError as exc:
            self._logger.debug("json decode error: %s", str(exc))
            self._logger.error("Unable to parse artifact file")
            return False

        version = data.get("version", "")
        if version.startswith("1."):
            try:
                stdout = data["stdout"]
                if self.mode == "interactive":
                    self._plays.value = data["plays"]
                    self._interaction.ui.update_status(data["status"], data["status_color"])
                    self.stdout = stdout
                else:
                    for line in data["stdout"]:
                        if self._args.display_color is True:
                            print(line)
                        else:
                            print(remove_ansi(line))
            except KeyError as exc:
                self._logger.debug("missing keys from artifact file")
                self._logger.debug("error was: %s", str(exc))
                return False
        else:
            self._logger.error(
                "Incompatible artifact version, got '%s', compatible = '1.y.z'", version
            )
            return False

        self._runner_finished = True
        self._logger.debug("Completed replay artifact request with mode %s", self.mode)
        return True

    def _prompt_for_artifact(self, artifact_file: str) -> Dict[Any, Any]:
        """prompt for a valid artifact file"""

        if not isinstance(artifact_file, str):
            artifact_file = ""

        FType = Dict[str, Any]
        form_dict: FType = {
            "title": "Artifact file not found, please confirm the following",
            "fields": [],
        }
        form_field = {
            "name": "artifact_file",
            "prompt": "Path to artifact file",
            "type": "text_input",
            "validator": {"name": "valid_file_path"},
            "pre_populate": artifact_file,
        }
        form_dict["fields"].append(form_field)
        form = dict_to_form(form_dict)
        self._interaction.ui.show(form)
        populated_form = form_to_dict(form, key_on_name=True)
        return populated_form

    def _prompt_for_playbook(self) -> Dict[Any, Any]:
        """prepopulate a form to confirm the playbook details"""

        self._logger.debug("Inventory/Playbook not set, provided, or valid, prompting")

        if isinstance(self._args.playbook, str):
            playbook = self._args.playbook
        else:
            playbook = ""

        if isinstance(self._args.inventory, list):
            inventory = self._args.inventory
        else:
            inventory = ["", "", ""]

        if isinstance(self._args.cmdline, list):
            cmdline = " ".join(self._args.cmdline)
        else:
            cmdline = ""

        FType = Dict[str, Any]
        form_dict: FType = {
            "title": "Inventory and/or playbook not found, please confirm the following",
            "fields": [],
        }
        form_field = {
            "name": "playbook",
            "pre_populate": playbook,
            "prompt": "Path to playbook",
            "type": "text_input",
            "validator": {"name": "valid_file_path"},
        }
        form_dict["fields"].append(form_field)

        for idx, inv in enumerate(inventory):
            form_field = {
                "name": f"inv_{idx}",
                "pre_populate": inv,
                "prompt": "Inventory source",
                "type": "text_input",
                "validator": {"name": "valid_path_or_none"},
            }
            form_dict["fields"].append(form_field)

        form_field = {
            "name": "cmdline",
            "pre_populate": cmdline,
            "prompt": "Additional command line parameters",
            "type": "text_input",
            "validator": {"name": "none"},
        }
        form_dict["fields"].append(form_field)
        form = dict_to_form(form_dict)
        self._interaction.ui.show(form)
        populated_form = form_to_dict(form, key_on_name=True)
        return populated_form

    def _take_step(self) -> None:
        """run the current step on the stack"""

        result = None
        if isinstance(self.steps.current, Interaction):
            result = run_action(self.steps.current.name, self.app, self.steps.current)
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
                    filter_content_keys=self._content_key_filter,
                )
        if result is None:
            self.steps.back_one()
        else:
            self.steps.append(result)

    def _run_runner(self) -> None:
        """spin up runner"""
        executable_cmd: Optional[str]

        if self.mode == "stdout_w_artifact":
            mode = "interactive"
        else:
            mode = self.mode

        if isinstance(self._args.set_environment_variable, dict):
            set_envvars = {**self._args.set_environment_variable}
        else:
            set_envvars = {}

        if self._args.display_color is False:
            set_envvars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "inventory": self._args.inventory,
            "navigator_mode": mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_envvars,
        }

        if isinstance(self._args.playbook, str):
            kwargs.update({"playbook": self._args.playbook})

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts}
            )

        if self._args.execution_environment:
            executable_cmd = "ansible-playbook"
        else:
            executable_cmd = shutil.which("ansible-playbook")
            if not executable_cmd:
                self._logger.error("'ansible-playbook' executable not found")
                return

        pass_through_arg = []
        if self._args.help_playbook is True:
            pass_through_arg.append("--help")
        if isinstance(self._args.cmdline, list):
            pass_through_arg.extend(self._args.cmdline)
        kwargs.update({"cmdline": pass_through_arg})

        self.runner = CommandRunnerAsync(executable_cmd=executable_cmd, queue=self._queue, **kwargs)
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
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-statements
        """Handle a runner message

        :param message: The message from runner
        :type message: dict
        """
        try:
            event = message["event"]
        except KeyError:
            error = f"Unhandled message from runner queue, discarded: {message}"
            self._logger.critical(error)
        else:
            if "stdout" in message and message["stdout"]:
                self.stdout.extend(message["stdout"].splitlines())
                if self.mode == "stdout_w_artifact":
                    print(message["stdout"])

            if event in ["verbose", "error"]:
                if "ERROR!" in message["stdout"]:
                    self._msg_from_plays = ("ERROR", 9)
                    if self.mode == "interactive":
                        self._notify_error(message["stdout"])
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
                    task_id = None
                    for idx, play_task in enumerate(self._plays.value[play_id]["tasks"]):
                        if task["task_uuid"] == play_task["task_uuid"]:
                            if task["host"] == play_task["host"]:
                                task_id = idx
                                break
                    if task_id is not None:
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
                new = floor((completed / task_count * 100))
                current = self._plays.value[idx].get("__pcomplete", 0)
                self._plays.value[idx]["__pcomplete"] = max(new, current)
                self._plays.value[idx]["__progress"] = str(max(new, current)) + "%"
            else:
                self._plays.value[idx]["__progress"] = "0%"

    def _prepare_to_quit(self, interaction: Interaction) -> bool:
        """Looks like we're headed out of here

        :param interaction: the quit interaction
        :type interaction: Interaction
        :return: a bool indicating whether of not it's safe to exit
        :rtype: bool
        """
        self.update()
        if self.runner is not None and not self.runner.finished:
            if interaction.action.match.groupdict()["exclamation"]:
                self._logger.debug("shutting down runner")
                self.runner.cancelled = True
                while not self.runner.finished:
                    pass
                self.write_artifact()
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
            columns=self._task_list_columns,
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

        if hasattr(self, "runner"):
            self._dequeue()
            self._set_status()

            if self.runner.finished and not self._runner_finished:
                # self._interaction.ui.disable_refresh()
                self._logger.debug("runner finished")
                self._logger.info("Playbook complete")
                self.write_artifact()
                self._runner_finished = True

    def _get_status(self) -> Tuple[str, int]:
        """Get the status and color

        :return: status string, status color
        :rtype: tuple of str and int
        """
        status = ""
        status_color = 0
        if self.runner.status:
            if self.runner and self.runner.finished and self.runner.status:
                status = self.runner.status
                if self.runner.status == "failed":
                    status_color = 9
                else:
                    status_color = self._msg_from_plays[1] or 10
            else:
                if self._msg_from_plays[0] is not None and self._msg_from_plays[1] is not None:
                    status = self._msg_from_plays[0]
                    status_color = self._msg_from_plays[1]
                else:
                    status = self.runner.status
                    status_color = 10
        return status, status_color

    def _set_status(self) -> None:
        """Set the ui status"""
        status, status_color = self._get_status()
        self._interaction.ui.update_status(status, status_color)

    def write_artifact(self, filename: Optional[str] = None) -> None:
        """Write the artifact

        :param filename: The file to write to
        :type filename: str
        """
        if (
            filename
            or self._args.playbook_artifact_enable is True
            and self._args.help_playbook is not True
        ):
            filename = filename or self._args.playbook_artifact_save_as
            filename = filename.format(
                playbook_dir=os.path.dirname(self._args.playbook),
                playbook_name=os.path.splitext(os.path.basename(self._args.playbook))[0],
                ts_utc=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
            )
            self._logger.debug("Formatted artifact file name set to %s", filename)
            filename = abs_user_path(filename)
            self._logger.debug("Resolved artifact file name set to %s", filename)

            status, status_color = self._get_status()

            try:
                os.makedirs(os.path.dirname(filename), exist_ok=True)
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

            except (IOError, OSError) as exc:
                error = (
                    f"Saving the artifact file failed, resulted in the following error: f{str(exc)}"
                )
                self._logger.error(error)

    def rerun(self) -> None:
        """rerun the current playbook
        since we're not reinstantiating run,
        drain the queue, clear the steps, reset the index, etc
        """
        if self._subaction_type == "run":
            if self.runner.finished:
                self._plays.value = []
                self._plays.index = None
                self._msg_from_plays = (None, None)
                self._queue.queue.clear()
                self.stdout = []
                self._run_runner()
                self.steps.clear()
                self.steps.append(self._plays)
                self._logger.debug("Playbook rerun triggered")
            else:
                self._logger.warning("Playbook rerun ignored, current playbook not complete")
        elif self._subaction_type == "replay":
            self._logger.error("No rerun available when artifact is loaded")
        else:
            self._logger.error("sub-action type '%s' is invalid", self._subaction_type)

    def _notify_error(self, message: str):
        """show a blocking warning"""
        warn_msg = ["Errors were encountered while running the playbook:"]
        messages = remove_ansi(message).splitlines()
        messages[-1] += "..."
        warn_msg.extend(messages)
        warn_msg += ["[HINT] To see the full error message try ':stdout'"]
        warn_msg += ["[HINT] After it's fixed, try to ':rerun' the playbook"]
        warning = warning_notification(warn_msg)
        self._interaction.ui.show(warning)
