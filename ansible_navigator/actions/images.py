""" :images """
import curses
import json
import shlex

from functools import partial

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from . import run_action
from . import _actions as actions

from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..image_manager import inspect_all
from ..runner.api import CommandRunner
from ..steps import Step

from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import nonblocking_notification
from ..ui_framework import warning_notification


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
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
class Action(App):
    """:images"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^im(?:ages)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="images")
        self._image_list: List = []
        self._images = Step(
            name="images",
            tipe="menu",
            columns=["__name", "tag", "execution_environment", "created", "size"],
            value=[],
            select_func=self._build_image_menu,
        )

    def color_menu(self, colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
        # pylint: disable=unused-argument

        """color the menu"""
        # images list menu
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

    def generate_content_heading(self, obj: Dict, screen_w: int, name: str = "") -> CursesLines:
        """generate the content heading"""
        if name == "image_menu":
            text = (
                self.steps.previous.selected["image_name"]
                + f" ({self.steps.previous.selected['description']})"
            )
        elif name in ["python_package_list", "system_package_list"]:
            text = f"{obj['name']} ({obj['version']})"

        color = 2
        if self._images.selected:
            if self._images.selected["__full_name"] == self._args.execution_environment_image:
                color = 4
            elif self._images.selected["execution_environment"] is False:
                color = 8

        empty_str = " " * (screen_w - len(text) + 1)
        heading_str = (text + empty_str).upper()
        heading = (
            (
                CursesLinePart(
                    column=0,
                    string=heading_str,
                    color=color,
                    decoration=curses.A_UNDERLINE | curses.A_BOLD,
                ),
            ),
        )
        return heading

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        """Handle :images

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("images requested")
        self._prepare_to_run(app, interaction)

        self._update_args(
            [self._name] + shlex.split(self._interaction.action.match.groupdict()["params"] or "")
        )

        notification = nonblocking_notification(
            messages=["Collecting available images, this may take a minute..."]
        )
        interaction.ui.show(notification)

        self._collect_image_list()
        if not self._images.value:
            messages = [
                "No images were found, or the configured container engine was not available."
            ]
            messages.append("Please check the log (:log) for errors.")
            warning = warning_notification(messages=messages)
            interaction.ui.show(warning)
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
        """take one step"""
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
                    self.generate_content_heading, name=self.steps.previous.name
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
        if self._images.selected is None:
            # an image should always be selected by now
            return self.steps.previous

        if self.steps.current.index == 0:
            step = Step(
                name="image_inspection",
                tipe="content",
                value=self._images.selected["inspect"],
            )
            return step

        if not self._images.selected["__introspected"]:
            message = "Collecting image details, this may take a minute..."
            notification = nonblocking_notification(messages=[message])
            self._interaction.ui.show(notification)
            self._introspect_image()

        if self.steps.current.index == 1:
            step = Step(
                name="general",
                tipe="content",
                value=self._images.selected["general"],
            )

        elif self.steps.current.index == 2:
            step = Step(
                name="ansible",
                tipe="content",
                value=self._images.selected["ansible"],
            )

        elif self.steps.current.index == 3:
            step = Step(
                columns=["name", "version", "summary"],
                name="python_package_list",
                tipe="menu",
                select_func=self._build_python_content,
                value=sorted(
                    self._images.selected["python"]["details"], key=lambda i: i["name"].lower()
                ),
            )

        elif self.steps.current.index == 4:
            step = Step(
                columns=["name", "version", "summary"],
                name="system_package_list",
                tipe="menu",
                select_func=self._build_system_content,
                value=sorted(
                    self._images.selected["system"]["details"], key=lambda i: i["name"].lower()
                ),
            )

        elif self.steps.current.index == 5:
            step = Step(
                name="everything",
                tipe="content",
                value=self.steps.previous.selected,
            )
        return step

    def _build_image_menu(self) -> Step:
        if self._images.selected is None:
            # an image should always be selected by now
            return self.steps.previous

        image_name = f"{self._images.selected['__name_tag']}"
        menu = [
            {
                image_name: "Image information",
                "description": "Information collected from image inspection",
            }
        ]
        if self.steps.current.selected["execution_environment"]:
            menu.append(
                {
                    image_name: "General information",
                    "description": "OS and python version information",
                }
            )
            menu.append(
                {
                    image_name: "Ansible version and collections",
                    "description": "Information about ansible and ansible collections",
                }
            )
            menu.append(
                {
                    image_name: "Python packages",
                    "description": "Information about python and python packages",
                }
            )
            menu.append(
                {
                    image_name: "Operating system packages",
                    "description": "Information about operating system packages",
                }
            )
            menu.append({image_name: "Everything", "description": "All image information"})
        for menu_entry in menu:
            menu_entry["image_name"] = image_name

        columns = [image_name, "description"]
        step = Step(
            columns=columns,
            name="image_menu",
            tipe="menu",
            value=menu,
            select_func=self._build_image_content,
        )
        self._interaction.ui.menu_filter(value=None)
        return step

    def _build_python_content(self) -> Step:
        return Step(
            name="python_content",
            tipe="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _build_system_content(self) -> Step:
        return Step(
            name="system_content",
            tipe="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _collect_image_list(self):
        images, error = inspect_all(container_engine=self._args.container_engine)
        if error or not images:
            self._logger.error(error)
            return

        for image in images:
            image["__introspected"] = False
            image["name"] = image["repository"].split("/")[-1]
            image["__name_tag"] = f"{image['name']}:{image['tag']}"
            image["__full_name"] = f"{image['repository']}:{image['tag']}"
            image["__name"] = image["name"]
            if image["__full_name"] == self._args.execution_environment_image:
                image["__name"] += " (primary)"
                image["__name_tag"] += " (primary)"

            try:
                image["execution_environment"] = (
                    image["inspect"]["details"]["config"]["working_dir"] == "/runner"
                )
            except KeyError:
                image["execution_environment"] = False
        self._images.value = sorted(images, key=lambda i: i["name"])

    def _introspect_image(self):

        self._images.selected["__introspected"] = True
        share_directory = self._args.internals.share_directory
        container_volume_mounts = [f"{share_directory}/utils:{share_directory}/utils:z"]
        python_exec_path = "python3"

        kwargs = {
            "cmdline": [f"{share_directory}/utils/image_introspect.py"],
            "container_engine": self._args.container_engine,
            "container_volume_mounts": container_volume_mounts,
            "execution_environment_image": self._images.selected["__full_name"],
            "execution_environment": True,
            "navigator_mode": "interactive",
        }
        self._logger.debug(
            f"Invoke runner with executable_cmd: {python_exec_path}" + f" and kwargs: {kwargs}"
        )
        _runner = CommandRunner(executable_cmd=python_exec_path, **kwargs)
        output, error = _runner.run()
        if not error:
            parsed = self._parse(output)
            self._images.selected["general"] = {
                "os": parsed["os_release"],
                "friendly": parsed["redhat_release"],
                "python": parsed["python_version"],
            }
            self._images.selected["ansible"] = {
                "ansible": {
                    "collections": parsed["ansible_collections"],
                    "version": parsed["ansible_version"],
                }
            }
            self._images.selected["python"] = parsed["python_packages"]
            self._images.selected["system"] = parsed["system_packages"]

    def _parse(self, output) -> None:
        """parse the introspection output"""
        # pylint: disable=too-many-branches
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
            return None

        for error in parsed["errors"]:
            self._logger.error("%s %s", error["path"], error["error"])
        return parsed
