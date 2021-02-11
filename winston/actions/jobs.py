""" :jobs
"""
import _thread
import copy
import datetime
import io
import logging
import os
import re
import threading

from argparse import Namespace

from collections import deque
from contextlib import redirect_stderr
from math import ceil

from typing import Any
from typing import Deque
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple
from typing import Union
from urllib.parse import urlparse

from awxkit.api import Connection  # type: ignore

from . import _actions as actions
from . import run as run_action

from .explore import PLAY_COLUMNS
from .explore import content_heading
from .explore import filter_content_keys

from ..app import App
from ..app_public import AppPublic


from ..steps import Step

from ..ui_framework import Interaction
from ..ui_framework import dict_to_form
from ..ui_framework import Form


from ..utils import human_time


DEFAULT_PAGE_SIZE = 25
RETRIEVER_THREADS = (os.cpu_count() or 4) - 1
DEQUE_RECHECK = 1
DEFAULT_TOWER_REFRESH = 2

# pylint: disable=inherit-non-class
class Config(NamedTuple):
    # pylint: disable=too-few-public-methods

    """the connection config"""

    url: str
    credentials: Union[Dict, None] = None
    token: Union[str, None] = None


class JobsCollector:
    """a job collector, uses a double ended queue
    to denote the priority of requests
    """

    def __init__(self, config: Config) -> None:
        self._logger = logging.getLogger(__name__)
        self._config = config
        self.jobs: List = []
        self._pending_queue: Deque = deque()
        self._completed_queue: Deque = deque()
        self._connection = Connection(self._config.url)

    def connect(self) -> bool:
        """connect to the host and
        ensure the connection is viable, start worker threads
        """
        self._connection.login(**self._config.credentials)
        viable = self._connection_viable(self._connection)
        if not viable:
            self._completed_queue.append({"error": "connection not viable"})
            return False
        for _thread_index in range(RETRIEVER_THREADS):
            _thread.start_new_thread(self._retriever, ())
        _thread.start_new_thread(self._message_processor, ())
        return True

    def full_stop(self) -> None:
        """stop the retrievers and processor threads"""
        for _thread_index in range(RETRIEVER_THREADS):
            self._pending_queue.append(None)
        self._completed_queue.append(None)
        self._connection.logout()

    def _connection_viable(self, connection: Connection) -> bool:
        """
        ensure the connection is authenticated and api v2 is available
        """
        fio = io.StringIO()
        with redirect_stderr(fio):
            try:
                response = connection.get("/api/v2/me")
                if not response:
                    return False
            except Exception as exc:  # pylint: disable=broad-except
                self._logger.error("Unable to connect to host")
                self._logger.debug("error: %s", str(exc))
                return False
        return True

    def _retriever(self) -> None:
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-branches
        """make call to the hosts api"""
        event = threading.Event()

        while True:
            if self._pending_queue:
                message = self._pending_queue.pop()
            else:
                event.wait(DEQUE_RECHECK)
                continue

            if message is None:
                break
            try:
                rest_result = self._connection.get(message["url"])
                self._logger.debug("retrieved: %s", message["url"])
            except Exception as exc:  # pylint: disable=broad-except
                self._logger.error("error retrieving: %s", message["url"])
                self._logger.debug("error retrieving: %s", str(exc))
                break

            if rest_result:
                rest_object = rest_result.json()
                if "page=" not in message["url"]:
                    expected = rest_object.get("count")
                    if expected is not None:
                        if expected > DEFAULT_PAGE_SIZE:
                            for page_no in range(2, ceil(expected / DEFAULT_PAGE_SIZE) + 1):
                                parsed = urlparse(message["url"])
                                if parsed.query:
                                    page_url = f"{message['url']}&page={page_no}"
                                else:
                                    page_url = f"{message['url']}?page={page_no}"
                                payload = {
                                    "url": page_url,
                                    "resource": message["resource"],
                                    "meta": message["meta"],
                                }
                                if "job_events" in page_url:
                                    self._pending_queue.append(payload)
                                else:
                                    self._pending_queue.appendleft(payload)
                    else:
                        self._logger.error("Missing count in initial get: %s", message["url"])

                results = rest_object.get("results")
                for result in results:
                    self._completed_queue.appendleft(
                        {
                            "resource": message["resource"],
                            "payload": result,
                            "meta": message["meta"],
                        }
                    )
            else:
                self._logger.error("Error retrieving resource: %s", message["url"])
                self._logger.error("Status code: %s", rest_result.status_code)
                self._logger.error("Response was: %s", rest_result.content.decode())

    def _message_processor(self) -> None:
        # pylint: disable=too-many-branches
        """process responses from the host api"""
        event = threading.Event()

        while True:
            if self._completed_queue:
                message = self._completed_queue.pop()
            else:
                event.wait(DEQUE_RECHECK)
                continue

            if message is None:
                break
            if message.get("resource") == "job":
                job = message["payload"]

                finished = job.get("finished")
                if finished is not None:
                    date_obj = datetime.datetime.fromisoformat(finished.replace("Z", "+00:00"))
                    job["__finished"] = date_obj.strftime("%Y-%m-%d %H:%M")
                else:
                    job["__finished"] = None

                job_idx = self.index_for_job_id(job["id"])
                if job_idx is not None:
                    job["events"] = self.jobs[job_idx]["events"]
                    job["events_collected"] = self.jobs[job_idx]["events_collected"]
                    self.jobs[job_idx] = job
                else:
                    job["events"] = []
                    job["events_collected"] = False
                    self.jobs.append(job)

            elif message.get("resource") == "job_event":
                job_id = message["meta"]["job_id"]
                job_idx = self.index_for_job_id(job_id=job_id)
                if job_idx is not None:
                    current_counters = [e["counter"] for e in self.jobs[job_idx]["events"]] or [0]
                    this_counter = message["payload"]["counter"]
                    if this_counter not in current_counters:
                        self.jobs[job_idx]["events"].append(message["payload"])
                        if message["payload"]["event"] == "playbook_on_stats":
                            self.jobs[job_idx]["events_collected"] = True

    def retrieve_jobs(self, since: Union[datetime.datetime, None] = None) -> None:
        """initial job retrieval"""
        url = "/api/v2/jobs/?order_by=-id"
        if since:
            date_str = since.replace(tzinfo=datetime.timezone.utc).isoformat()
            date_str = date_str.replace("+00:00", "Z")
            url = (
                f"{url}&or__created__gte={date_str}&"
                f"or__finished__gte={date_str}&"
                f"or__modified__gte={date_str}"
            )
            self._pending_queue.append({"url": url, "resource": "job", "meta": {}})
        else:
            self._pending_queue.appendleft({"url": url, "resource": "job", "meta": {}})

    def index_for_job_id(self, job_id: int) -> Union[None, int]:
        """convenience method to get a job index
        from the list of jobs given it's ID
        """
        job_idx = next(
            (index for (index, job) in enumerate(self.jobs) if job["id"] == job_id), None
        )
        return job_idx

    def retrieve_events_for_job(
        self, job_id: int, since: Union[datetime.datetime, None] = None
    ) -> None:
        """retrieve events for a job"""
        job_idx = self.index_for_job_id(job_id)
        if job_idx is None:
            return

        job = self.jobs[job_idx]

        if job["status"] == "pending":
            return

        url = f"{job['related']['job_events']}?order_by=created"
        if since:
            date_str = since.replace(tzinfo=datetime.timezone.utc).isoformat()
            date_str = date_str.replace("+00:00", "Z")
            url = f"{url}&or__created__gte={date_str}&" f"or__modified__gte={date_str}"

        self._pending_queue.append(
            {"url": url, "resource": "job_event", "meta": {"job_id": job_id}}
        )
        return


JOB_COLUMNS = ["name", "id", "status", "description", "__finished"]

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


RESULT_TO_COLOR = [
    ("(?i)^failed$", 9),
    ("(?i)^ok$", 10),
    ("(?i)^ignored$", 13),
    ("(?i)^skipped$", 14),
    ("(?i)^in_progress$", 8),
]

get_color = lambda word: next((x[1] for x in RESULT_TO_COLOR if re.match(x[0], word)), 0)


def color_jobs_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=unused-argument

    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """
    color = 0
    if entry["status"] == "successful":
        color = 10
    elif entry["status"] == "failed":
        color = 9
    elif entry["status"] == "pending":
        color = 8
    elif entry["status"] == "running":
        color = 11
    return color


def color_plays_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=unused-argument
    """color the menu of plays"""
    colval = entry[colname]
    color = 0
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
    return color


def color_tasks_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=unused-argument
    """color the menu of tasks"""
    colval = entry[colname]
    color = 0
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


@actions.register
class Action(App):
    """:inventory"""

    # pylint:disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes

    KEGEX = r"^j(?:obs)?(\s(?P<params>.*))?$"

    def __init__(self, args: Namespace) -> None:
        super().__init__(args=args)
        self._name_at_cli: str = "jobs"
        self._calling_app: AppPublic
        self._logger = logging.getLogger(__name__)
        self._parser_error: str
        self._interaction: Interaction

        self._jobs = Step(
            name="jobs",
            tipe="menu",
            columns=JOB_COLUMNS,
            value=[],
            show_func=self._jobs_sort,
            select_func=self._job_selected,
        )
        self._plays = Step(
            name="plays",
            tipe="menu",
            columns=PLAY_COLUMNS,
            value=[],
            show_func=self._update_plays_from_job,
            select_func=self._task_list_for_play,
        )
        self._selected_job_id: Union[int, None] = None
        self._jobs_collector: JobsCollector
        self._job_events_handled: List[int] = []
        self._last_update: datetime.datetime
        self._msg_from_plays: str = ""

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        # pylint: disable=too-many-branches
        """Handle :inventory

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("jobs requested")
        self._calling_app = app
        self.args = app.args
        self._interaction = interaction

        config = self._ensure_arguments()
        if config is None:
            return None
        self._jobs_collector = JobsCollector(config=config)

        connected = self._jobs_collector.connect()
        if connected is False:
            self._logger.error("unable to connect to tower host, check url and credentials")
            return None

        self._last_update = datetime.datetime.utcnow()
        self._jobs_collector.retrieve_jobs()
        self._jobs.value = self._jobs_collector.jobs

        self.steps.append(self._jobs)
        previous_scroll = interaction.ui.scroll()
        previous_filter = interaction.ui.menu_filter()
        self._interaction.ui.scroll(0)

        while True:
            self.update()
            self._take_step()

            if not self.steps:
                if self.args.app == self.name:
                    self.steps.append(self._jobs)
                else:
                    break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._jobs_collector.full_stop()
        interaction.ui.scroll(previous_scroll)
        interaction.ui.menu_filter(previous_filter)
        return None

    def _take_step(self) -> None:

        result = None
        if isinstance(self.steps.current, Interaction):
            result = run_action(
                self.steps.current.name,
                self.app,
                self.steps.current,
            )
        elif isinstance(self.steps.current, Step):
            if self.steps.current.show_func:
                current_index = self.steps.current.index
                self.steps.current.show_func()
                self.steps.current.index = current_index

            if self.steps.current.type == "menu":
                if self.steps.current.name == "jobs":
                    color_func = color_jobs_menu
                elif self.steps.current.name == "plays":
                    color_func = color_plays_menu
                else:
                    color_func = color_tasks_menu

                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=color_func,
                )
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

    def parser_error(self, message: str) -> Tuple[None, None]:
        """callback for parser error

        :param message: A message from the parser
        :type message: str
        """
        self._parser_error = message
        return None, None

    def _ensure_arguments(self) -> Union[None, Config]:
        """ensure the arguments are present to retrieve jobs"""
        params = self._interaction.action.match.groupdict().get("params")
        if params:
            self._logger.debug("Using params provided in interaction")
            params = [self._name_at_cli] + params.split()
            new_args = self._update_args(params)
            if new_args is None:
                return None
        else:
            self._logger.debug("Using params from calling app")
            new_args = copy.copy(self._calling_app.args)

        self.args = new_args

        if not self.confirm_connection_requirements():
            form_response = self._prompt_for_connection_details()
            for field in form_response.fields:
                if field.name.startswith("tower_"):
                    setattr(self.args, field.name, field.response)
            if not self.confirm_connection_requirements():
                return None

        if getattr(self.args, "tower_token", None):
            config = Config(url=self.args.tower_url, token=self.args.tower_token)
        else:
            config = Config(
                url=self.args.tower_url,
                credentials={
                    "username": self.args.tower_username,
                    "password": self.args.tower_password,
                },
            )

        return config

    def confirm_connection_requirements(self) -> bool:
        """check for url + token or u/p"""
        connection_requirements = True
        if not getattr(self.args, "tower_url", None):
            connection_requirements = False
        if not (
            getattr(self.args, "tower_token", None)
            or (
                getattr(self.args, "tower_username", None)
                and getattr(self.args, "tower_password", None)
            )
        ):
            connection_requirements = False
        return connection_requirements

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
            arg_value = getattr(args, key, None)
            if arg_value != value:
                self._logger.debug(
                    "Overriding previous cli param '%s:%s' with '%s:%s'", key, arg_value, key, value
                )
                setattr(args, key, value)
        return args

    def _prompt_for_connection_details(self) -> Form:
        """genrate connection detail form
        and present to the user
        """
        FType = Dict[str, Any]
        form_dict: FType = {
            "title": "Please provide a URL and credentials",
            "fields": [],
        }
        form_field = {
            "name": "tower_url",
            "pre_populate": getattr(self.args, "tower_url", None),
            "prompt": "URL",
            "type": "text_input",
            "validator": {"name": "http"},
        }
        form_dict["fields"].append(form_field)
        form_field = {
            "name": "tower_username",
            "pre_populate": getattr(self.args, "tower_username", None),
            "prompt": "Username",
            "type": "text_input",
            "validator": {"name": "none"},
        }
        form_dict["fields"].append(form_field)
        form_field = {
            "name": "tower_password",
            "pre_populate": getattr(self.args, "tower_password", None),
            "prompt": "Password",
            "type": "text_input",
            "validator": {"name": "masked_or_none"},
        }
        form_dict["fields"].append(form_field)
        form_field = {
            "name": "tower_token",
            "pre_populate": getattr(self.args, "tower_token", None),
            "prompt": "Token",
            "type": "text_input",
            "validator": {"name": "masked_or_none"},
        }
        form_dict["fields"].append(form_field)
        form = dict_to_form(form_dict)
        self._interaction.ui.show(form)
        return form

    def _job_selected(self) -> Step:
        """trigger event collection for a job

        :return: The menu step
        :rtype: Step
        """
        self._selected_job_id = self.steps.current.selected["id"]
        self._job_events_handled = []
        self._plays.value = []
        self._msg_from_plays = ""
        self._interaction.ui.menu_filter(None)
        self._update()
        return self._plays

    def _jobs_sort(self) -> None:
        self._jobs_collector.jobs.sort(
            key=lambda k: (k["__finished"] is None, k["__finished"]), reverse=True
        )

    def update(self) -> None:
        """update the calling app
        and the host data based on time elapsed
        """
        self._calling_app.update()
        current_time = datetime.datetime.utcnow()
        if (current_time - self._last_update).total_seconds() > getattr(
            self.app.args, "tower_refresh", DEFAULT_TOWER_REFRESH
        ):
            self._update()
            self._logger.debug("periodic refresh initiated")
            self._last_update = current_time

    def _update(self) -> None:
        self._jobs_collector.retrieve_jobs(since=self._last_update)
        if self._selected_job_id is not None:
            job_idx = self._jobs_collector.index_for_job_id(self._selected_job_id)
            if job_idx is not None:
                current_job = self._jobs_collector.jobs[job_idx]
                if current_job["events_collected"] is False:
                    self._jobs_collector.retrieve_events_for_job(job_id=self._selected_job_id)
                    current_job["events_collected"] = "in_progress"
                elif current_job["events_collected"] == "in_progress":
                    self._jobs_collector.retrieve_events_for_job(
                        job_id=self._selected_job_id, since=self._last_update
                    )

                self.stdout.clear()
                for event in self._jobs_collector.jobs[job_idx]["events"]:
                    if "stdout" in event and event["stdout"]:
                        self.stdout.extend(event["stdout"].splitlines())

    def _update_plays_from_job(self) -> None:
        """update the details of the Play
        using the events from the job, skip previously used events
        """
        if self._selected_job_id is not None:
            job_idx = self._jobs_collector.index_for_job_id(self._selected_job_id)
            if job_idx is not None:
                selected_job = self._jobs_collector.jobs[job_idx]

                for idx, event in enumerate(selected_job["events"]):
                    if idx not in self._job_events_handled:
                        result = self._handle_message(event)
                        if result is True:
                            self._job_events_handled.append(idx)

                self._plays.value.sort(key=lambda k: k["__event_index"])
                for play in self._plays.value:
                    play["tasks"].sort(key=lambda k: k["__event_index"])
                    for idx, task in enumerate(play["tasks"]):
                        task["__number"] = idx

                self._play_stats()

    def _handle_message(self, message: dict) -> bool:
        # pylint: disable=too-many-branches
        """Handle a job event

        :param message: The event
        :type message: dict
        """
        event = message["event"]

        if event in ["verbose", "error"]:
            if "ERROR!" in message["stdout"]:
                self._msg_from_plays = "ERROR"
            elif "WARNING" in message["stdout"] and self._msg_from_plays != "ERROR":
                self._msg_from_plays = "WARNINGS"

        elif event == "playbook_on_play_start":
            play = message["event_data"]
            play["__event_index"] = message["counter"]
            play["__play_name"] = play["name"]
            play["tasks"] = []
            self._plays.value.append(play)

        elif event.startswith("runner_on_"):
            runner_event = event.split("_")[2]
            task = message["event_data"]
            play_id = next(
                (idx for idx, p in enumerate(self._plays.value) if p["uuid"] == task["play_uuid"]),
                None,
            )
            if play_id is None:
                self._logger.debug("play not found for event, retry later")
                return False

            task_idx = None
            for idx, play_task in enumerate(self._plays.value[play_id]["tasks"]):
                if task["task_uuid"] == play_task["task_uuid"]:
                    if task["host"] == play_task["host"]:
                        task_idx = idx
                        break

            if runner_event in ["ok", "skipped", "unreachable", "failed"]:
                if task_idx is None:
                    self._logger.debug("runner start event not seen yet")
                    return False
                if runner_event == "failed" and task["ignore_errors"]:
                    result = "ignored"
                else:
                    result = runner_event
                task["__result"] = result.upper()
                task["__changed"] = task.get("res", {}).get("changed", False)
                task["__duration"] = human_time(seconds=round(task["duration"], 2))
                self._plays.value[play_id]["tasks"][task_idx].update(task)

            elif runner_event == "start":
                if task_idx is None:
                    task["__host"] = task["host"]
                    task["__result"] = "IN_PROGRESS"
                    task["__changed"] = "unknown"
                    task["__duration"] = None
                    task["__event_index"] = message["counter"]
                    task["__task"] = task["task"]
                    task["__task_action"] = task["task_action"]
                    self._plays.value[play_id]["tasks"].append(task)
        return True

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

    def _task_list_for_play(self) -> Step:
        """generate a menu of tasks for the currently selected play

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
