""" explorer
"""
import json

from collections import deque
from queue import Queue
from typing import Deque
from typing import Tuple
from typing import Union

import winston.actions as actions

from .app import App
from .playbook_runner import PlaybookRunner
from .player_ui_callbacks import color_menu_item
from .player_ui_callbacks import content_heading
from .player_ui_callbacks import filter_content_keys
from .step import Step
from .ui import Interaction
from .ui import UserInterface
from .utils import human_time


DEFAULT_REFRESH = 100


class Player(App):

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """the playbook ui"""

    def __init__(self, args):
        super().__init__(args)

        self._queue = Queue()
        self._task_cache = {}
        self.runner = None
        self._runner_finished = None

        self.stdout = []

        self.actions = actions
        self._ui = None
        self._msg_from_plays = (None, None)
        self._plays = Step("plays", "menu", self._play_stats)
        self._tasks = Step("tasks", "menu", lambda x: x["tasks"])
        self._task = Step("task", "content", None)

        self._plays.previous = self._plays
        self._plays.next = self._tasks
        self._plays.columns = [
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

        self._tasks.previous = self._plays
        self._tasks.next = self._task
        self._tasks.columns = [
            "result",
            "host",
            "number",
            "changed",
            "task",
            "task action",
            "duration",
        ]

        self._task.previous = self._tasks
        self._task.next = None

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
                # if self.args.stream and not self.args.quiet:
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

    def _load_artifact(self) -> None:
        """Load the artifact from the fs or kick off runner"""
        self._logger.debug("Starting load artifact request")

        with open(self.args.artifact) as json_file:
            data = json.load(json_file)
        self._plays.value = data["plays"]
        self._ui.status = data["status"]
        self._ui.status_color = data["status_color"]
        self.stdout = data["stdout"]
        self._logger.debug("Completed load artifact request")

    def _run_runner(self) -> None:
        """ spin up runner """
        self._logger.debug("Starting playbook run request")
        self.runner = PlaybookRunner(args=self.args, queue=self._queue)
        self.runner.run()
        self._runner_finished = False
        self._logger.debug("Completed playbook run request")

    @staticmethod
    def _play_stats(step: Step) -> None:
        """Calculate the play's stats based
        on it's tasks
        """
        for idx, play in enumerate(step.value):
            total = ["ok", "skipped", "failed", "unreachable", "ignored", "in progress"]
            step.value[idx].update(
                {
                    tot: len([t for t in play["tasks"] if t["result"].lower() == tot])
                    for tot in total
                }
            )
            step.value[idx]["changed"] = len([t for t in play["tasks"] if t["changed"] is True])
            task_count = len(play["tasks"])
            step.value[idx]["task count"] = task_count
            completed = task_count - step.value[idx]["in progress"]
            if completed:
                new = round((completed / task_count * 100))
                current = step.value[idx].get("_pcomplete", 0)
                step.value[idx]["_pcomplete"] = max(new, current)
                step.value[idx]["% completed"] = str(max(new, current)) + "%"
            else:
                step.value[idx]["% completed"] = "0%"

    def _populate_step(self) -> None:
        """Populate the data for the step"""
        if self.step == self.step.previous:
            self.step.func(self.step)
            return

        if self.step.func is None:
            return

        if self.step.previous.selected:
            if self.step.previous.changed or not self.step.value:
                self.step.value = self.step.func(self.step.previous.selected)
        return

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
        self._ui.status = status
        self._ui.status_color = status_color

    def _prepare_to_quit(self, interaction: Interaction) -> Union[bool, None]:
        """Looks like we're headed out of here

        :param result: the result from the ui
        :type result: dict
        """
        if not self.runner.finished:
            if interaction.action.match.groupdict()["exclamation"]:
                self._logger.debug("shutting down runner")
                self.runner.cancelled = True
                while not self.runner.finished:
                    pass
                if filename := self.args.artifact:
                    self.write_artifact(filename)
                return True
            self._logger.warning("Quit requested but playbook running, try q! or quit!")
            return None
        self._logger.debug("runner not running")
        return True

    def update(self) -> None:
        """Drain the queue, set the status and write the artifact if needed"""
        if self.runner:
            self._dequeue()
            self._set_status()

            if self.runner.finished and not self._runner_finished:
                self._ui.disable_refresh()
                self._logger.debug("runner finished, disabled refresh")
                if filename := self.args.artifact:
                    self.write_artifact(filename)
                self._runner_finished = True

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

    def rerun(self) -> None:
        if self.runner.finished:
            self._plays.value = []
            self._plays.index = None
            self._msg_from_plays = (None, None)
            self._queue.queue.clear()
            self.stdout = []
            self.step = self._plays
            self._run_runner()
            self.initialize_ui()
            self._logger.debug("Playbook rerun triggered")
        else:
            self._logger.warning("Playbook rerun ignored, current playbook not complete")

    def playbook(self) -> None:
        """Run in oldschool mode, just stdout"""
        self._run_runner()
        while True:
            self._dequeue()
            if self.runner.finished:
                if self.args.artifact:
                    self.write_artifact(self.args.artifact)
                self._logger.debug("runner finished")
                break

    def initialize_ui(self, refresh: int = DEFAULT_REFRESH) -> None:
        """initialize the user interface

        :param refresh: The refresh for the ui
        :type refresh: int
        """
        self._ui = UserInterface(
            screen_miny=3,
            no_osc4=self.args.no_osc4,
            kegexes=self.actions.kegexes,
            refresh=refresh,
            share_dir=self.args.share_dir,
        )

    def explore(self, _screen) -> None:
        # pylint: disable=too-many-branches
        """Run with the interface and runner"""
        self.initialize_ui()
        self._run_runner()
        self.step = self._plays
        self._run_app()

    def load(self, _screen) -> None:
        """ Run with the interface and load artifact"""
        self.initialize_ui(-1)
        self._load_artifact()
        self.step = self._plays
        self._run_app()

    def _run_app(self) -> None:
        """enter the endless loop"""

        # pylint: disable=too-many-branches
        ique: Deque = deque()
        while True:
            if self.args.app == "explore":
                self.update()

            if ique:
                interaction = self.actions.run(
                    action=ique[-1].action.name,
                    app=self,
                    interaction=ique[-1],
                )
            elif self.step.type == "menu":
                self._populate_step()
                interaction = self._ui.show(
                    obj=self.step.value, columns=self.step.columns, color_menu_item=color_menu_item
                )

            elif self.step.type == "content":
                interaction = self._ui.show(
                    obj=self.step.previous.value,
                    index=self.step.previous.index,
                    content_heading=content_heading,
                    filter_content_keys=filter_content_keys,
                )

            if isinstance(interaction, Interaction):
                if interaction.action.name == "quit":
                    if self.args.app == "load":
                        return
                    if self.args.app == "explore":
                        self.update()
                        done = self._prepare_to_quit(interaction)
                        if done:
                            return
                        if ique:
                            ique.pop()
                elif ique and interaction.action.name == "back":
                    ique.pop()
                else:
                    ique.append(interaction)
            elif isinstance(interaction, bool):
                # true, stay on current action
                # false, step back one, or return to steps
                ique.pop()
                if interaction is False and ique:
                    ique.pop()
            else:
                self._logger.debug("Invalid response from action: %s", interaction)
                interaction = False
