"""Images subcommand implementation."""
from __future__ import annotations

import curses
import json
import shlex

from copy import deepcopy
from functools import partial
from typing import Any

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.image_manager import inspect_all
from ansible_navigator.runner import Command
from ansible_navigator.steps import Step
from ansible_navigator.ui_framework import CursesLine
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import CursesLines
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import nonblocking_notification
from ansible_navigator.ui_framework import warning_notification
from ansible_navigator.utils.print import print_to_stdout

from . import _actions as actions
from . import run_action


def filter_content_keys(obj: dict[Any, Any]) -> dict[Any, Any]:
    """Filter out some keys when showing image content.

    :param obj: The object from which keys should be removed
    :returns: The object with keys removed
    """
    if isinstance(obj, list):
        working = [filter_content_keys(x) for x in obj]
        return working
    if isinstance(obj, dict):
        working = {}
        for k, val in obj.items():
            if not k.startswith("__"):
                working[k] = filter_content_keys(val)
        return working
    return obj


@actions.register
class Action(ActionBase):
    """Images subcommand implementation."""

    KEGEX = r"^im(?:ages)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:images`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="images")
        self._image_list: list = []
        self._images = Step(
            name="images",
            step_type="menu",
            columns=["__image", "tag", "execution_environment", "created", "size"],
            value=[],
            select_func=self._build_image_menu,
        )

    def color_menu(self, colno: int, colname: str, entry: dict[str, Any]) -> tuple[int, int]:
        """Provide a color for a images menu entry in one column.

        :param colno: The column number
        :param colname: The column name
        :param entry: The menu entry
        :returns: The color and decoration
        """
        if "__full_name" in entry:
            if entry.get("execution_environment") is False:
                return 8, 0
            if entry["__full_name"] == self._args.execution_environment_image:
                return 12, 0
            return 2, 0

        if self._images.selected:
            if self._images.selected["execution_environment"] is False:
                return 8, 0
            if self._images.selected["__full_name"] == self._args.execution_environment_image:
                return 12, 0
        return 2, 0

    def generate_content_heading(self, obj: dict, screen_w: int, name: str = "") -> CursesLines:
        """Create a heading for image content.

        :param obj: The content going to be shown
        :param screen_w: The current screen width
        :param name: The name of the images menu
        :returns: The heading
        """
        if name == "image_menu":
            text = (
                f"{self.steps.previous.selected['first_column']}"
                f" ({self.steps.previous.selected['description']})"
            )
        elif name in ["python_package_list", "system_package_list"]:
            text = f"Name: {obj['name']} ({obj['version']})"

        color = 2
        if self._images.selected:
            if self._images.selected["__full_name"] == self._args.execution_environment_image:
                color = 4
            elif self._images.selected["execution_environment"] is False:
                color = 8

        empty_str = " " * (screen_w - len(text) + 1)
        heading_str = text + empty_str
        line_part = CursesLinePart(
            column=0,
            string=heading_str,
            color=color,
            decoration=curses.A_UNDERLINE,
        )
        return CursesLines((CursesLine((line_part,)),))

    def run_stdout(self) -> RunStdoutReturn:
        """Handle settings in mode stdout.

        :returns: RunStdoutReturn
        """
        self._logger.debug("images requested in stdout mode")

        details_source = self._args.entry("images_details").value.source
        if details_source is not Constants.DEFAULT_CFG:
            return self.run_stdout_details()

        self._collect_image_list()
        if not self._images.value:
            msg = "No images were found, or the configured container engine was not available."
            return RunStdoutReturn(message=msg, return_code=1)
        filtered = []
        for image in self._images.value:
            if image["execution_environment"] is False:
                continue
            image["name_tag"] = image["__name_tag"]
            image["full_name"] = image["__full_name"]
            filtered.append(filter_content_keys(image))
        print_to_stdout(
            content=filtered,
            content_format=getattr(ContentFormat, self._args.format.upper()),
            use_color=self._args.display_color,
        )
        return RunStdoutReturn(message="", return_code=0)

    def run_stdout_details(self) -> RunStdoutReturn:
        """Execute the ``images --details`` request for mode stdout.

        :returns: A message and return code
        """
        image_name = self._args.execution_environment_image

        output, error, return_code = self._run_runner(image_name=image_name)
        if error or return_code:
            return RunStdoutReturn(message=error, return_code=return_code)

        details = self._parse(output)
        if details is None:
            message = "Image introspection failed, please check the logs and log an issue."
            return RunStdoutReturn(message=message, return_code=1)

        details.pop("errors")
        sections = self._args.entry("images_details").value.current
        for section_name, section in deepcopy(details).items():
            if section_name not in sections and "everything" not in sections:
                details.pop(section_name)
            else:
                for key in section:
                    if key.startswith("__"):
                        details[section_name].pop(key)

        details["image_name"] = image_name
        print_to_stdout(
            content=details,
            content_format=ContentFormat.YAML,
            use_color=self._args.display_color,
        )
        return RunStdoutReturn(message="", return_code=0)

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction | None:
        """Execute the ``images`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("images requested")
        self._prepare_to_run(app, interaction)

        args_updated = self._update_args(
            [self._name] + shlex.split(self._interaction.action.match.groupdict()["params"] or ""),
        )
        if not args_updated:
            self._prepare_to_exit(interaction)
            return None

        notification = nonblocking_notification(
            messages=["Collecting available images, this may take a minute..."],
        )
        interaction.ui.show_form(notification)

        self._collect_image_list()
        if not self._images.value:
            messages = [
                "No images were found, or the configured container engine was not available.",
            ]
            messages.append("Please check the log (:log) for errors.")
            warning = warning_notification(messages=messages)
            interaction.ui.show_form(warning)
            self._logger.error(messages[0])
            return None

        self.steps.append(self._images)

        while True:
            self._calling_app.update()
            self._take_step()

            if not self.steps:
                break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._prepare_to_exit(interaction)
        return None

    def _take_step(self) -> None:
        """Take a step based on the current step or step back."""
        result = None
        if isinstance(self.steps.current, Interaction):
            result = run_action(self.steps.current.name, self.app, self.steps.current)
        elif isinstance(self.steps.current, Step):
            if self.steps.current.show_func:
                current_index = self.steps.current.index
                self.steps.current.show_func()
                self.steps.current.index = current_index

            if self.steps.current.type == "menu":
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=self.color_menu,
                )
            elif self.steps.current.type == "content":
                content_heading = partial(
                    self.generate_content_heading,
                    name=self.steps.previous.name,
                )
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

    def _build_image_content(self) -> Step:
        """Build the menu of image details.

        :returns: The image details menu definition
        """
        if self._images.selected is None:
            # an image should always be selected by now
            return self.steps.previous

        if self.steps.current.index == 0:
            step = Step(
                name="image_inspection",
                step_type="content",
                value=self._images.selected["inspect"],
            )
            return step

        if not self._images.selected["__introspected"]:
            message = "Collecting image details, this may take a minute..."
            notification = nonblocking_notification(messages=[message])
            self._interaction.ui.show_form(notification)
            introspection_success = self._introspect_image()
            if introspection_success is False:
                return self.steps.previous

        if self.steps.current.index == 1:
            step = Step(
                name="general",
                step_type="content",
                value=self._images.selected["general"],
            )

        elif self.steps.current.index == 2:
            step = Step(
                name="ansible",
                step_type="content",
                value=self._images.selected["ansible"],
            )

        elif self.steps.current.index == 3:
            step = Step(
                columns=["name", "version", "summary"],
                name="python_package_list",
                step_type="menu",
                select_func=self._build_python_content,
                value=sorted(
                    self._images.selected["python"]["details"],
                    key=lambda i: i["name"].lower(),
                ),
            )

        elif self.steps.current.index == 4:
            step = Step(
                columns=["name", "version", "summary"],
                name="system_package_list",
                step_type="menu",
                select_func=self._build_system_content,
                value=sorted(
                    self._images.selected["system"]["details"],
                    key=lambda i: i["name"].lower(),
                ),
            )

        elif self.steps.current.index == 5:
            step = Step(
                name="everything",
                step_type="content",
                value=self.steps.previous.selected,
            )
        return step

    def _build_image_menu(self) -> Step:
        """Build the menu of images.

        :returns: The images menu definition
        """
        if self._images.selected is None:
            # an image should always be selected by now
            return self.steps.previous

        first_column = f"Image: {self._images.selected['__name_tag']}"
        menu = [
            {
                first_column: "Image information",
                "description": "Information collected from image inspection",
            },
        ]
        if self.steps.current.selected["execution_environment"]:
            menu.append(
                {
                    first_column: "General information",
                    "description": "OS and python version information",
                },
            )
            menu.append(
                {
                    first_column: "Ansible version and collections",
                    "description": "Information about ansible and ansible collections",
                },
            )
            menu.append(
                {
                    first_column: "Python packages",
                    "description": "Information about python and python packages",
                },
            )
            menu.append(
                {
                    first_column: "Operating system packages",
                    "description": "Information about operating system packages",
                },
            )
            menu.append({first_column: "Everything", "description": "All image information"})
        for menu_entry in menu:
            menu_entry["first_column"] = first_column

        columns = [first_column, "description"]
        step = Step(
            columns=columns,
            name="image_menu",
            step_type="menu",
            value=menu,
            select_func=self._build_image_content,
        )
        self._interaction.ui.menu_filter(value=None)
        return step

    def _build_python_content(self) -> Step:
        """Build the content for an image's python packages.

        :returns: The python package content
        """
        return Step(
            name="python_content",
            step_type="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _build_system_content(self) -> Step:
        """Build the content for an image's system packages.

        :returns: The system package content
        """
        return Step(
            name="system_content",
            step_type="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _collect_image_list(self):
        """Build a list of images for the images menu."""
        images, error = inspect_all(container_engine=self._args.container_engine)
        if error or not images:
            self._logger.error(error)
            return

        for image in images:
            image["__introspected"] = False
            image["name"] = image["repository"].split("/")[-1]
            image["__image"] = image["name"]
            image["__name_tag"] = f"{image['name']}:{image['tag']}"
            image["__full_name"] = f"{image['repository']}:{image['tag']}"
            image["__name"] = image["name"]
            if image["__full_name"] == self._args.execution_environment_image:
                image["__name"] += " (primary)"
                image["__name_tag"] += " (primary)"

            details = image["inspect"]["details"]

            try:
                legacy_check = details["config"]["working_dir"] == "/runner"
            except KeyError:
                legacy_check = False

            # podman has a root label
            try:
                root_label_check = details["labels"]["ansible-execution-environment"] == "true"
            except (KeyError, TypeError):
                root_label_check = False

            # docker has only a config.label
            try:
                config_label_check = (
                    details["config"]["labels"]["ansible-execution-environment"] == "true"
                )
            except (KeyError, TypeError):
                config_label_check = False

            image["execution_environment"] = any(
                (legacy_check, root_label_check, config_label_check)
            )
        self._images.value = sorted(images, key=lambda i: i["name"])

    def _introspect_image(self) -> bool:
        """Use the runner subsystem to introspect an image.

        :returns: An indication of image introspection success
        """
        if self._images.selected is None:
            # an image should always be selected by now
            return False

        self._images.selected["__introspected"] = True

        output, error, _return_code = self._run_runner(
            image_name=self._images.selected["__full_name"],
        )

        if error:
            self._logger.error(
                "Image introspection failed (runner), the return value was: %s",
                error,
            )
            self.notify_failed()
            return False
        parsed = self._parse(output)
        if parsed is None:
            self.notify_failed()
            return False

        try:
            self._images.selected["general"] = {
                "os": parsed["os_release"],
                "friendly": parsed["redhat_release"],
                "python": parsed["python_version"],
            }
            self._images.selected["ansible"] = {
                "ansible": {
                    "collections": parsed["ansible_collections"],
                    "version": parsed["ansible_version"],
                },
            }
            self._images.selected["python"] = parsed["python_packages"]
            self._images.selected["system"] = parsed["system_packages"]
        except KeyError:
            self._logger.exception(
                "Image introspection failed (keys), the return value was: %s",
                output[0:1000],
            )
            self.notify_failed()
            return False
        return True

    def _parse(self, output) -> dict | None:
        """Load and process the ``json`` output from the image introspection process.

        :param output: The output from the image introspection process
        :returns: The parsed output
        """
        try:
            if not output.startswith("{"):
                _warnings, json_str = output.split("{", 1)
                json_str = "{" + json_str
            else:
                json_str = output
            parsed = json.loads(json_str)
            self._logger.debug("json loading output succeeded")
        except (json.decoder.JSONDecodeError, ValueError) as exc:
            self._logger.error("Unable to extract introspection from stdout")
            self._logger.debug("error json loading output: '%s'", str(exc))
            self._logger.debug(output)
            self._logger.error(
                "Image introspection failed (parsed), the return value was: %s",
                output[0:1000],
            )
            return None

        for error in parsed["errors"]:
            self._logger.error("%s %s", error["path"], error["error"])
        return parsed

    def _run_runner(self, image_name: str) -> tuple[str, str, int]:
        """Run runner to collect image details.

        :param image_name: The full image name
        :returns: Output, errors and the return code
        """
        cache_path = self._args.internals.cache_path
        container_volume_mounts = [f"{cache_path}:{cache_path}"]
        python_exec_path = "/usr/bin/python3"

        kwargs = {
            "cmdline": [f"{cache_path}/image_introspect.py"],
            "container_engine": self._args.container_engine,
            "container_volume_mounts": container_volume_mounts,
            "execution_environment_image": image_name,
            "execution_environment": True,
            "navigator_mode": "interactive",
        }

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        self._logger.debug(
            "Invoke runner with executable_cmd: %s and kwargs: %s", python_exec_path, kwargs
        )
        _runner = Command(executable_cmd=python_exec_path, **kwargs)
        output, error, return_code = _runner.run()
        return output, error, return_code

    def notify_failed(self):
        """Notify image introspection failed."""
        msgs = ["humph. Something went really wrong while introspecting the image."]
        msgs.append("Details have been added to the log file")
        closing = ["[HINT] Please log an issue about this one, it shouldn't have happened"]
        warning = warning_notification(messages=msgs + closing)
        self._interaction.ui.show_form(warning)
