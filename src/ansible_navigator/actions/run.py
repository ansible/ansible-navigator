"""Run subcommand implementation."""
import curses
import json
import logging
import os
import re
import shlex
import shutil
import time
import uuid

from math import floor
from pathlib import Path
from queue import Queue
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from ..action_base import ActionBase
from ..action_defs import RunStdoutReturn
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..content_defs import ContentView
from ..content_defs import SerializationFormat
from ..runner import CommandAsync
from ..steps import Step
from ..ui_framework import CursesLine
from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import dict_to_form
from ..ui_framework import form_to_dict
from ..ui_framework import nonblocking_notification
from ..ui_framework import warning_notification
from ..utils.functions import abs_user_path
from ..utils.functions import human_time
from ..utils.functions import now_iso
from ..utils.functions import remove_ansi
from ..utils.functions import round_half_up
from ..utils.serialize import serialize_write_file
from . import _actions as actions
from . import run_action


RESULT_TO_COLOR = [
    ("(?i)^failed$", 9),
    ("(?i)^ok$", 10),
    ("(?i)^ignored$", 13),
    ("(?i)^skipped$", 14),
    ("(?i)^in_progress$", 8),
]

get_color = lambda word: next(  # noqa: E731
    (x[1] for x in RESULT_TO_COLOR if re.match(x[0], word)),
    0,
)


def color_menu(_colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    # pylint: disable=too-many-branches
    """Find matching color for word.

    :param colname: The column name
    :param entry: The menu entry
    :returns: The color and decoration
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


def content_heading(obj: Any, screen_w: int) -> Optional[CursesLines]:
    """Create a heading for some piece of content showing.

    :param obj: The content going to be shown
    :param screen_w: The current screen width
    :returns: The heading
    """
    if isinstance(obj, dict) and "task" in obj:
        detail = f"PLAY [{obj['play']}:{obj['__number']}] "
        stars = "*" * (screen_w - len(detail))

        line_1 = CursesLine(
            (CursesLinePart(column=0, string=detail + stars, color=0, decoration=0),),
        )

        detail = f"TASK [{obj['task']}] "
        stars = "*" * (screen_w - len(detail))
        line_2 = CursesLine(
            (CursesLinePart(column=0, string=detail + stars, color=0, decoration=0),),
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

        string = f"{res}: [{obj['__host']}] {msg}"
        string = string + (" " * (screen_w - len(string) + 1))
        line_3 = CursesLine(
            (CursesLinePart(column=0, string=string, color=color, decoration=curses.A_UNDERLINE),),
        )

        return CursesLines((line_1, line_2, line_3))
    return None


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """Filter out some keys when showing collection content.

    :param obj: The object from which keys should be removed
    :returns: The object with keys removed
    """
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
class Action(ActionBase):

    # pylint: disable=too-many-instance-attributes
    """Run command implementation."""

    KEGEX = r"""(?x)
            ^
            (?P<run>r(?:un)?
            (\s(?P<params_run>.*))?)
            $"""

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:run`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="run")

        self._subaction_type: str
        self._msg_from_plays: Tuple[Optional[str], Optional[int]] = (None, None)
        self._queue: Queue = Queue()
        self.runner: CommandAsync
        self._runner_finished: bool
        self._auto_scroll = False
        #: Flag when the first message is received from runner
        self._first_message_received: bool = False

        self._plays = Step(
            name="plays",
            step_type="menu",
            columns=PLAY_COLUMNS,
            value=[],
            show_func=self._play_stats,
            select_func=self._task_list_for_play,
        )
        self._task_list_columns: List[str] = TASK_LIST_COLUMNS
        self._content_key_filter: Callable = filter_content_keys

    @property
    def mode(self):
        """Determine the mode and if playbook artifact creation is enabled.

        If so, run in interactive mode, but print stdout.

        :returns: If stdout and artifact creation, return a str statement as such, else return mode
        """
        if all(
            (
                self._args.mode == "stdout",
                self._args.playbook_artifact_enable,
                self._args.app != "replay",
            ),
        ):
            return "stdout_w_artifact"
        return self._args.mode

    def run_stdout(self) -> RunStdoutReturn:
        """Execute the ``inventory`` request for mode stdout.

        :returns: The return code from the runner invocation, along with a message to review the
            logs if not 0
        """
        if self._args.app == "replay":
            successful: bool = self._init_replay()
            if successful:
                return RunStdoutReturn(message="", return_code=0)
            return RunStdoutReturn(message="Please review the log for errors.", return_code=1)

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
            # Sleep briefly to prevent 100% CPU utilization
            # in mode stdout, the delay introduced by the curses key read is not present
            time.sleep(0.01)
        return_code = self.runner.ansible_runner_instance.rc
        if return_code != 0:
            return RunStdoutReturn(
                message="Please review the log for errors.",
                return_code=return_code,
            )
        return RunStdoutReturn(message="", return_code=return_code)

    def run(self, interaction: Interaction, app: AppPublic) -> Optional[Interaction]:
        """Run :run or :replay.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending interaction or none
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

        # Show a notification until the first the first message from the queue is processed
        if self._subaction_type == "run":
            messages = ["Preparing for automation, please wait..."]
            notification = nonblocking_notification(messages=messages)
            interaction.ui.show_form(notification)
            while not self._first_message_received:
                self.update()

        while True:
            self.update()

            self._take_step()

            if not self.steps:
                if not self._runner_finished:
                    self._logger.error("Can not step back while playbook in progress, :q! to exit")
                    self.steps.append(self._plays)
                else:
                    self._logger.debug(
                        "No steps remaining for '%s' returning to calling app",
                        self._name,
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
        """In the case of :run, check the user input.

        :returns: True
        """
        # Ensure the playbook and inventory are valid

        args_updated = self._update_args(
            ["run"] + shlex.split(self._interaction.action.match.groupdict()["params_run"] or ""),
        )
        if not args_updated:
            return False

        if isinstance(self._args.playbook, str):
            playbook_valid = os.path.exists(self._args.playbook)
        else:
            playbook_valid = False

        if not playbook_valid:

            populated_form = self._prompt_for_playbook()
            if populated_form["cancelled"]:
                return False

            new_cmd = ["run"]
            new_cmd.append(populated_form["fields"]["playbook"]["value"])

            if populated_form["fields"]["cmdline"]["value"]:
                new_cmd.extend(shlex.split(populated_form["fields"]["cmdline"]["value"]))

            # Parse as if provided from the cmdline
            args_updated = self._update_args(new_cmd)
            if not args_updated:
                return False

        self._run_runner()
        self._logger.info("Run initialized and playbook started.")
        return True

    def _init_replay(self) -> bool:
        """In the case of :replay, replay the artifact.

        Check for a version and process artifact file.

        :returns: True if replay completes, False if there is an error
        """
        self._logger.debug("Starting replay artifact request with mode %s", self.mode)

        if self.mode == "interactive":
            args_updated = self._update_args(
                ["replay"]
                + shlex.split(self._interaction.action.match.groupdict()["params_replay"] or ""),
            )
            if not args_updated:
                return False

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
            with open(artifact_file, encoding="utf-8") as fh:
                data = json.load(fh)
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
                "Incompatible artifact version, got '%s', compatible = '1.y.z'",
                version,
            )
            return False

        self._runner_finished = True
        self._logger.debug("Completed replay artifact request with mode %s", self.mode)
        return True

    def _prompt_for_artifact(self, artifact_file: str) -> Dict[Any, Any]:
        """Prompt for a valid artifact file.

        :param artifact_file: Artifact file
        :returns: Dict with artifact detail entries
        """
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
        self._interaction.ui.show_form(form)
        populated_form = form_to_dict(form, key_on_name=True)
        return populated_form

    def _prompt_for_playbook(self) -> Dict[Any, Any]:
        """Prepopulate a form to confirm the playbook details.

        :returns: Dict with playbook and inventory detail entries
        """
        self._logger.debug("Inventory/Playbook not set, provided, or valid, prompting")

        if isinstance(self._args.playbook, str):
            playbook = self._args.playbook
        else:
            playbook = ""

        if isinstance(self._args.cmdline, list):
            cmdline = " ".join(self._args.cmdline)
        else:
            cmdline = ""

        FType = Dict[str, Any]
        form_dict: FType = {
            "title": "Playbook not found, please confirm the following",
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

        form_field = {
            "name": "cmdline",
            "pre_populate": cmdline,
            "prompt": "Additional command line parameters",
            "type": "text_input",
            "validator": {"name": "none"},
        }
        form_dict["fields"].append(form_field)
        form = dict_to_form(form_dict)
        self._interaction.ui.show_form(form)
        populated_form = form_to_dict(form, key_on_name=True)
        return populated_form

    def _take_step(self) -> None:
        """Run the current step on the stack."""
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
        """Spin up runner.

        :raises RuntimeError: If no ansible-playbook executable
        """
        executable_cmd: Optional[str]

        if self.mode == "stdout_w_artifact":
            mode = "interactive"
        else:
            mode = self.mode

        if isinstance(self._args.set_environment_variable, dict):
            set_env_vars = {**self._args.set_environment_variable}
        else:
            set_env_vars = {}

        if self._args.display_color is False:
            set_env_vars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "inventory": self._args.inventory,
            "navigator_mode": mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_env_vars,
            "private_data_dir": self._args.ansible_runner_artifact_dir,
            "rotate_artifacts": self._args.ansible_runner_rotate_artifacts_count,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.playbook, str):
            kwargs.update({"playbook": self._args.playbook})

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts},
            )

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        if self._args.execution_environment:
            executable_cmd = "ansible-playbook"
        else:
            executable_cmd = shutil.which("ansible-playbook")
            if not executable_cmd:
                msg = "'ansible-playbook' executable not found"
                self._logger.error(msg)
                raise RuntimeError(msg)

        pass_through_arg = []
        if self._args.help_playbook is True:
            pass_through_arg.append("--help")
        if isinstance(self._args.cmdline, list):
            pass_through_arg.extend(self._args.cmdline)
        kwargs.update({"cmdline": pass_through_arg})

        self.runner = CommandAsync(executable_cmd=executable_cmd, queue=self._queue, **kwargs)
        self.runner.run()
        self._runner_finished = False
        self._logger.debug("runner requested to start")

    def _dequeue(self) -> None:
        """Drain the runner queue."""
        drain_count = 0
        while not self._queue.empty():
            if not self._first_message_received:
                self._first_message_received = True
            message = self._queue.get()
            self._handle_message(message)
            drain_count += 1
        if drain_count:
            self._logger.debug("Drained %s events", drain_count)

    def _handle_message(self, message: dict) -> None:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-statements
        """Handle a runner message.

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
                    task["__task"] = task["task"]
                    task["__result"] = result.upper()
                    task["__changed"] = task.get("res", {}).get("changed", False)
                    if isinstance(task["duration"], (int, float)):
                        task["__duration"] = human_time(seconds=round_half_up(task["duration"]))
                    else:
                        msg = (
                            f"Task duration for '{task['task']}' was type {type(task['duration'])},"
                            " set to 0"
                        )
                        self._logger.debug(msg)
                        task["__duration"] = 0

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
        """Calculate the play's stats based on it's tasks."""
        for idx, play in enumerate(self._plays.value):
            total = ["__ok", "__skipped", "__failed", "__unreachable", "__ignored", "__in_progress"]
            self._plays.value[idx].update(
                {
                    tot: len([t for t in play["tasks"] if t["__result"].lower() == tot[2:]])
                    for tot in total
                },
            )
            self._plays.value[idx]["__changed"] = len(
                [t for t in play["tasks"] if t["__changed"] is True],
            )
            task_count = len(play["tasks"])
            self._plays.value[idx]["__task_count"] = task_count
            completed = task_count - self._plays.value[idx]["__in_progress"]
            if completed:
                new = floor((completed / task_count * 100))
                current = self._plays.value[idx].get("__percent_complete", 0)
                self._plays.value[idx]["__percent_complete"] = max(new, current)
                self._plays.value[idx]["__progress"] = str(max(new, current)) + "%"
            else:
                self._plays.value[idx]["__progress"] = "0%"

    def _prepare_to_quit(self, interaction: Interaction) -> bool:
        """Pre-quit tasks.

        :param interaction: The quit interaction
        :returns: A bool indicating whether or not it's safe to exit
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
        """Generate a menu of tasks for the currently selected play.

        :returns: The menu step
        """
        value = self.steps.current.selected["tasks"]
        step = Step(
            name="task_list",
            step_type="menu",
            columns=self._task_list_columns,
            select_func=self._task_from_task_list,
            value=value,
        )
        return step

    def _task_from_task_list(self) -> Step:
        """Generate task content for the selected task.

        :returns: Content which shows a task
        """
        value = self.steps.current.value
        index = self.steps.current.index
        step = Step(name="task", step_type="content", index=index, value=value)
        return step

    def update(self) -> None:
        """Drain the queue, set the status and write the artifact if needed."""
        # let the calling app update as well
        self._calling_app.update()

        if hasattr(self, "runner"):
            self._dequeue()
            self._set_status()

            if self.runner.finished and not self._runner_finished:
                self._logger.debug("runner finished")
                self._logger.info("Playbook complete")
                self.write_artifact()
                self._runner_finished = True

    def _get_status(self) -> Tuple[str, int]:
        """Get the runner status and color for status message.

        :returns: status string, status color
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
        """Set the UI status."""
        status, status_color = self._get_status()
        self._interaction.ui.update_status(status, status_color)

    def write_artifact(self, filename: Optional[str] = None) -> None:
        """Write the artifact.

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
                time_stamp=now_iso(self._args.time_zone),
            )
            self._logger.debug("Formatted artifact file name set to %s", filename)
            filename = abs_user_path(filename)
            self._logger.debug("Resolved artifact file name set to %s", filename)

            status, status_color = self._get_status()

            try:
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                artifact = {
                    "version": "1.0.0",
                    "plays": self._plays.value,
                    "stdout": self.stdout,
                    "status": status,
                    "status_color": status_color,
                }
                serialize_write_file(
                    content=artifact,
                    content_view=ContentView.NORMAL,
                    file_mode="w",
                    file=Path(filename),
                    serialization_format=SerializationFormat.JSON,
                )
                self._logger.info("Saved artifact as %s", filename)

            except (IOError, OSError) as exc:
                error = (
                    f"Saving the artifact file failed, resulted in the following error: f{str(exc)}"
                )
                self._logger.error(error)

    def rerun(self) -> None:
        """Rerun the current playbook.

        Since we're not reinstating run, drain the queue,
        clear the steps, reset the index, etc.
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
        """Show a blocking warning.

        :param message: Message for warning
        """
        warn_msg = ["Errors were encountered while running the playbook:"]
        messages = remove_ansi(message).splitlines()
        messages[-1] += "..."
        warn_msg.extend(messages)
        warn_msg += ["[HINT] To see the full error message try ':stdout'"]
        warn_msg += ["[HINT] After it's fixed, try to ':rerun' the playbook"]
        warning = warning_notification(warn_msg)
        self._interaction.ui.show_form(warning)
