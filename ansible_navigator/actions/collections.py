""" :doc """
import curses
import json
import os
import shlex
import sys

from copy import deepcopy
from json.decoder import JSONDecodeError

from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Tuple

from . import run_action
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..runner.api import CommandRunner
from ..steps import Step

from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import nonblocking_notification
from ..ui_framework import warning_notification


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    # pylint: disable=unused-argument

    """color the menu"""
    if entry.get("__shadowed") is True:
        return 8, 0
    if entry.get("__deprecated") is True:
        return 9, 0
    return 2, 0


def content_heading(obj: Any, screen_w: int) -> Union[CursesLines, None]:
    """create a heading for host showing

    :param obj: The content going to be shown
    :type obj: Any
    :param screen_w: The current screen width
    :type screen_w: int
    :return: The heading
    :rtype: Union[CursesLines, None]
    """

    heading = []
    string = f"{obj['full_name'].upper()}: {obj['__description']}"
    string = string + (" " * (screen_w - len(string) + 1))

    heading.append(
        tuple(
            [
                CursesLinePart(
                    column=0,
                    string=string,
                    color=2,
                    decoration=curses.A_UNDERLINE,
                )
            ]
        )
    )
    return tuple(heading)


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    return {k: v for k, v in obj.items() if not k.startswith("__")}


@actions.register
class Action(App):
    """:doc"""

    # pylint:disable=too-few-public-methods
    # pylint:disable=too-many-instance-attributes

    KEGEX = r"^collections(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="collections")
        self._adjacent_collection_dir: str
        self._collection_cache: Dict
        self._collection_cache_path: str
        self._collection_scanned_paths: List = []
        self._collections: List = []
        self._stats: Dict = {}

    def update(self):
        self._calling_app.update()

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("collections requested")
        self._prepare_to_run(app, interaction)
        self.stdout = self._calling_app.stdout

        notification = nonblocking_notification(
            messages=[
                "Collecting collection content, this may take a minute the first time...",
            ]
        )
        interaction.ui.show(notification)

        params = [self._name] + shlex.split(
            self._interaction.action.match.groupdict()["params"] or ""
        )

        self._update_args(params=params, attach_cdc=True)
        self._collection_cache = self._args.internals.collection_doc_cache
        self._collection_cache_path = self._args.collection_doc_cache_path

        self._run_runner()

        if not self._collections:
            self._prepare_to_exit(interaction)
            self.notify_none()
            return None

        self.steps.append(self._build_main_menu())

        while True:
            self.update()
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
                    color_menu_item=color_menu,
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

    def _build_main_menu(self):
        """build the main menu of options"""
        if self._args.execution_environment:
            columns = ["__name", "__version", "__shadowed", "__type", "path"]
        else:
            columns = ["__name", "__version", "__shadowed", "path"]

        return Step(
            name="all_collections",
            columns=columns,
            select_func=self._build_plugin_menu,
            tipe="menu",
            value=self._collections,
        )

    def _build_plugin_menu(self):
        self._collection_cache.open()
        selected_collection = self._collections[self.steps.current.index]
        cname_col = f"__{selected_collection['known_as']}"
        plugins = []
        for plugin_chksum, details in selected_collection["plugin_chksums"].items():
            try:
                plugin_json = self._collection_cache[plugin_chksum]
                loaded = json.loads(plugin_json)

                plugin = loaded["plugin"]
                if plugin["doc"] is not None:
                    if "name" in plugin["doc"]:
                        short_name = plugin["doc"]["name"]
                    else:
                        short_name = plugin["doc"][details["type"]]
                    plugin[cname_col] = short_name
                    plugin["full_name"] = f"{selected_collection['known_as']}.{short_name}"
                    plugin["__type"] = details["type"]
                    plugin["collection_info"] = selected_collection["collection_info"]
                    plugin["collection_info"]["name"] = selected_collection["known_as"]
                    plugin["collection_info"]["shadowed_by"] = selected_collection["hidden_by"]
                    plugin["collection_info"]["path"] = selected_collection["path"]

                    plugin["__added"] = plugin["doc"].get("version_added")
                    plugin["__description"] = plugin["doc"]["short_description"]

                    runtime_section = "modules" if details["type"] == "module" else details["type"]
                    plugin["__deprecated"] = False
                    try:
                        rinfo = selected_collection["runtime"]["plugin_routing"][runtime_section][
                            short_name
                        ]
                        plugin["additional_information"] = rinfo
                        if "deprecation" in rinfo:
                            plugin["__deprecated"] = True
                    except KeyError:
                        plugin["additional_information"] = {}

                    plugins.append(plugin)
            except (KeyError, JSONDecodeError) as exc:
                self._logger.error("error loading plguin doc %s", details)
                self._logger.debug("error was %s", str(exc))
        plugins = sorted(plugins, key=lambda i: i[cname_col])
        self._collection_cache.close()

        return Step(
            name="all_plugins",
            columns=[cname_col, "__type", "__added", "__deprecated", "__description"],
            select_func=self._build_plugin_content,
            tipe="menu",
            value=plugins,
        )

    def _build_plugin_content(self):
        """build the content for one option"""
        return Step(
            name="plugin_content",
            tipe="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _run_runner(self) -> None:
        """spin up runner"""

        if isinstance(self._args.set_environment_variable, dict):
            set_environment_variable = deepcopy(self._args.set_environment_variable)
        else:
            set_environment_variable = {}
        set_environment_variable.update({"ANSIBLE_NOCOLOR": "True"})

        kwargs = {
            "container_engine": self._args.container_engine,
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": "interactive",
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_environment_variable,
        }

        if isinstance(self._args.playbook, str):
            playbook_dir = os.path.dirname(self._args.playbook)
        else:
            playbook_dir = os.getcwd()

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts}
            )

        kwargs.update({"host_cwd": playbook_dir})

        self._adjacent_collection_dir = os.path.join(playbook_dir, "collections")
        share_directory = self._args.internals.share_directory

        pass_through_arg = [
            f"{share_directory}/utils/catalog_collections.py",
            "-a",
            self._adjacent_collection_dir,
            "-c",
            self._collection_cache_path,
        ]

        kwargs.update({"cmdline": pass_through_arg})

        if self._args.execution_environment:
            self._logger.debug("running collections command with execution environment enabled")
            python_exec_path = "python3"

            container_volume_mounts = [f"{share_directory}/utils:{share_directory}/utils:z"]
            if os.path.exists(self._adjacent_collection_dir):
                container_volume_mounts.append(
                    f"{self._adjacent_collection_dir}:{self._adjacent_collection_dir}:z"
                )

            container_volume_mounts.append(
                f"{self._collection_cache_path}:{self._collection_cache_path}:z"
            )
            kwargs.update({"container_volume_mounts": container_volume_mounts})

        else:
            self._logger.debug("running collections command locally")
            python_exec_path = sys.executable

        self._logger.debug(
            f"Invoke runner with executable_cmd: {python_exec_path}" + f" and kwargs: {kwargs}"
        )
        _runner = CommandRunner(executable_cmd=python_exec_path, **kwargs)
        output, error = _runner.run()

        if error:
            msg = f"Error while running catalog collection script: {error}"
            self._logger.error(msg)
        if output:
            self._parse(output)

    def _parse(self, output) -> None:
        """yaml load the list, and parse the dump
        merge dump int list
        """
        # pylint: disable=too-many-branches
        try:
            if not output.startswith("{"):
                _warnings, json_str = output.split("{", 1)
                json_str = "{" + json_str
            else:
                json_str = output
            parsed = json.loads(json_str)
            self._logger.debug("json loading output succeeded")
        except (JSONDecodeError, ValueError) as exc:
            self._logger.error("Unable to extract collection json from stdout")
            self._logger.debug("error json loading output: '%s'", str(exc))
            self._logger.debug(output)
            return None

        for error in parsed["errors"]:
            self._logger.error("%s %s", error["path"], error["error"])

        self._collections = sorted(
            list(parsed["collections"].values()), key=lambda i: i["known_as"]
        )
        for collection in self._collections:
            collection["__name"] = collection["known_as"]
            collection["__version"] = collection["collection_info"].get("version", "missing")
            collection["__shadowed"] = bool(collection["hidden_by"])
            if self._args.execution_environment:
                if collection["path"].startswith(self._adjacent_collection_dir):
                    collection["__type"] = "bind_mount"
                elif collection["path"].startswith(os.path.dirname(self._adjacent_collection_dir)):
                    collection["__type"] = "bind_mount"
                    error = (
                        f"{collection['known_as']} was mounted and catalogued in the"
                        " execution environment but was outside the adjacent 'collections'"
                        " directory. This may cause issues outside the local development"
                        " environment."
                    )
                    self._logger.error(error)
                else:
                    collection["__type"] = "contained"

        self._stats = parsed["stats"]

        if parsed.get("messages"):
            for msg in parsed["messages"]:
                self._logger.info("[catalog_collections]: %s", msg)

        self._logger.debug("catalog collections scan path: %s", parsed["collection_scan_paths"])
        self._collection_scanned_paths = parsed["collection_scan_paths"].split(":")
        for stat, value in self._stats.items():
            self._logger.debug("%s: %s", stat, value)

        if not parsed["collections"]:
            env = "execution" if self._args.execution_environment else "local"
            error = f"No collections found in {env} environment, searched in "
            error += parsed["collection_scan_paths"]
            self._logger.warning(error)

        return None

    def notify_none(self):
        """notify no collections were found"""
        msgs = ["humph. no collections were found in the following paths:"]
        paths = []
        for path in self._collection_scanned_paths:
            if path.startswith(self._args.internals.share_directory):
                continue
            if self._args.execution_environment:
                if path.startswith(self._adjacent_collection_dir):
                    paths.append(f"- {path} (bind_mount)")
                else:
                    paths.append(f"- {path} (contained)")
            else:
                paths.append(f"- {path}")
        closing = ["[HINT] Try installing some or try a different execution enviroment"]
        warning = warning_notification(messages=msgs + paths + closing)
        self._interaction.ui.show(warning)
