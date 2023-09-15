"""Collections subcommand implementation."""
from __future__ import annotations

import curses
import json
import os
import shlex
import sys

from copy import deepcopy
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any
from typing import cast

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.runner import Command
from ansible_navigator.steps import Step
from ansible_navigator.ui_framework import CursesLine
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import CursesLines
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import nonblocking_notification
from ansible_navigator.ui_framework import warning_notification
from ansible_navigator.utils.functions import path_is_relative_to
from ansible_navigator.utils.functions import remove_dbl_un
from ansible_navigator.utils.key_value_store import KeyValueStore
from ansible_navigator.utils.print import print_to_stdout

from . import _actions as actions
from . import run_action


def color_menu(colno: int, colname: str, entry: dict[str, Any]) -> tuple[int, int]:
    """Provide a color for a collections menu entry in one column.

    :param colno: The column number
    :param colname: The column name
    :param entry: The menu entry
    :returns: The color and decoration
    """
    if entry.get("__shadowed") is True:
        return 8, 0
    if entry.get("__deprecated") == "True":
        return 9, 0
    return 2, 0


def content_heading(obj: Any, screen_w: int) -> CursesLines | None:
    """Create a heading for collection content.

    :param obj: The content going to be shown
    :param screen_w: The current screen width
    :returns: The heading
    """
    name = f"Image: {obj['full_name']}"
    description = f"Description: {obj['__description']}"
    padding = " " * (screen_w - len(description) + 1)
    line_1_part_1 = CursesLinePart(
        column=0,
        string=name,
        color=0,
        decoration=curses.A_NORMAL,
    )
    line_2_part_1 = CursesLinePart(
        column=0,
        string=description + padding,
        color=0,
        decoration=curses.A_UNDERLINE,
    )
    return CursesLines((CursesLine((line_1_part_1,)), CursesLine((line_2_part_1,))))


def filter_content_keys(obj: dict[Any, Any]) -> dict[Any, Any]:
    """Filter out some keys when showing collection content.

    :param obj: The object from which keys should be removed
    :returns: The object with keys removed
    """
    return {k: v for k, v in obj.items() if not k.startswith("__")}


@actions.register
class Action(ActionBase):
    """Collections subcommand implementation."""

    KEGEX = r"^collections(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``collections`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="collections")
        self._adjacent_collection_dir: str
        self._collection_cache: KeyValueStore
        self._collection_cache_path: str
        self._collection_scanned_paths: list = []
        self._collections: list = []
        self._stats: dict = {}

    def update(self) -> None:
        """Request calling app update, no collection update is required."""
        self._calling_app.update()

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction | None:
        """Execute the ``collections`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("collections requested")
        self._prepare_to_run(app, interaction)
        self.stdout = self._calling_app.stdout

        notification = nonblocking_notification(
            messages=[
                "Collecting collection content, this may take a minute the first time...",
            ],
        )
        interaction.ui.show_form(notification)

        params = [self._name] + shlex.split(
            self._interaction.action.match.groupdict()["params"] or "",
        )

        args_updated = self._update_args(params=params, attach_cdc=True)
        if not args_updated:
            self._prepare_to_exit(interaction)
            return None

        if not isinstance(self._args.internals.collection_doc_cache, KeyValueStore):
            notification = warning_notification(
                messages=[
                    "Something has gone really wrong, the collection document cache is not",
                    "available.  This should not have happened. Please log an issue, and",
                    "include the contents of the log file.",
                ],
            )
            interaction.ui.show_form(notification)
            self._prepare_to_exit(interaction)
            return None

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

    def run_stdout(self) -> RunStdoutReturn:
        """Execute the ``collection`` request for mode stdout.

        :returns: The return code or 1. If the response from the runner invocation is None,
            indicates there is no console output to display, so assume an issue and return 1
            along with a message to review the logs.
        """
        self._logger.debug("collection requested in stdout mode")

        args_updated = self._update_args(params=[], attach_cdc=True)
        if not args_updated or not isinstance(
            self._args.internals.collection_doc_cache,
            KeyValueStore,
        ):
            msg = (
                "Failed to create collections cache, "
                "Please review the ansible-navigator log file for errors."
            )
            return RunStdoutReturn(message=msg, return_code=1)

        self._collection_cache = self._args.internals.collection_doc_cache
        self._collection_cache_path = self._args.collection_doc_cache_path

        self._run_runner()
        if not self._collections:
            msg = (
                "Failed to catalog collections, "
                "Please review the ansible-navigator log file for errors."
            )
            return RunStdoutReturn(message=msg, return_code=1)

        collections_info = self._parse_collection_info_stdout()

        print_to_stdout(
            content=collections_info,
            content_format=getattr(ContentFormat, self._args.format.upper()),
            use_color=self._args.display_color,
        )
        return RunStdoutReturn(message="", return_code=0)

    def notify_failed(self):
        """Notify collection cataloging failed."""
        msgs = ["humph. Something went really wrong while cataloging collections."]
        msgs.append("Details have been added to the log file")
        closing = ["[HINT] Please log an issue about this one, it shouldn't have happened"]
        warning = warning_notification(messages=msgs + closing)
        self._interaction.ui.show_form(warning)

    def notify_none(self):
        """Notify no collections were found."""
        msgs = ["humph. no collections were found in the following paths:"]
        paths = []
        for path in self._collection_scanned_paths:
            if path.startswith(self._args.internals.cache_path):
                continue
            if self._args.execution_environment:
                if path.startswith(self._adjacent_collection_dir):
                    paths.append(f"- {path} (bind_mount)")
                else:
                    paths.append(f"- {path} (contained)")
            else:
                paths.append(f"- {path}")
        closing = ["[HINT] Try installing some or try a different execution environment"]
        warning = warning_notification(messages=msgs + paths + closing)
        self._interaction.ui.show_form(warning)

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
        """Build the menu of collections.

        :returns: The collections menu definition
        """
        if self._args.execution_environment:
            columns = ["__name", "__version", "__shadowed", "__type", "path"]
        else:
            columns = ["__name", "__version", "__shadowed", "path"]

        return Step(
            name="all_collections",
            columns=columns,
            select_func=self._build_collection_content_menu,
            step_type="menu",
            value=self._collections,
        )

    def _build_collection_content_menu(self):
        """Build the menu of plugins.

        :returns: The plugin menu definition
        """
        self._collection_cache.open_()
        selected_collection = self._collections[self.steps.current.index]
        collection_name = f"__{selected_collection['known_as']}"
        collection_contents = []
        for plugin_checksum, details in selected_collection["plugin_checksums"].items():
            try:
                plugin_json = self._collection_cache[plugin_checksum]
                loaded = json.loads(plugin_json)

                plugin = loaded["plugin"]
                if plugin["doc"] is not None:
                    if "name" in plugin["doc"]:
                        short_name = plugin["doc"]["name"]
                    else:
                        short_name = plugin["doc"][details["type"]]
                    plugin[collection_name] = short_name
                    plugin["full_name"] = f"{selected_collection['known_as']}.{short_name}"
                    plugin["__type"] = details["type"]
                    plugin["collection_info"] = selected_collection["collection_info"]
                    plugin["collection_info"]["name"] = selected_collection["known_as"]
                    plugin["collection_info"]["shadowed_by"] = selected_collection["hidden_by"]
                    plugin["collection_info"]["path"] = selected_collection["path"]

                    plugin["__added"] = plugin["doc"].get("version_added")
                    plugin["__description"] = plugin["doc"]["short_description"]

                    runtime_section = "modules" if details["type"] == "module" else details["type"]
                    plugin["__deprecated"] = "False"
                    try:
                        routing_info = selected_collection["runtime"]["plugin_routing"]
                        runtime_info = routing_info[runtime_section][short_name]
                        plugin["additional_information"] = runtime_info
                        if "deprecation" in runtime_info:
                            plugin["__deprecated"] = "True"
                    except KeyError:
                        plugin["additional_information"] = {}

                    collection_contents.append(plugin)
            except (KeyError, JSONDecodeError) as exc:
                self._logger.error("error loading plugin doc %s", details)
                self._logger.debug("error was %s", str(exc))

        self._collection_cache.close()

        for role in selected_collection["roles"]:
            role[collection_name] = role["short_name"]
            try:
                role["__description"] = role["info"]["galaxy_info"]["description"]
            except KeyError:
                role["__description"] = ""
            role["__deprecated"] = "Unknown"
            role["__added"] = "Unknown"
            role["__type"] = "role"
            collection_contents.append(role)

        collection_contents = sorted(collection_contents, key=lambda i: i[collection_name])

        return Step(
            name="all_collection_content",
            columns=[collection_name, "__type", "__added", "__deprecated", "__description"],
            select_func=self._build_collection_content,
            step_type="menu",
            value=collection_contents,
        )

    def _build_collection_content(self):
        """Build the content for one plugin.

        :returns: The plugin's content
        """
        return Step(
            name="collection_content",
            step_type="content",
            value=self.steps.current.value,
            index=self.steps.current.index,
        )

    def _run_runner(self) -> None:
        # pylint: disable=too-many-locals
        """Use the runner subsystem to catalog collections."""
        if isinstance(self._args.set_environment_variable, dict):
            set_environment_variable = deepcopy(self._args.set_environment_variable)
        else:
            set_environment_variable = {}
        set_environment_variable["ANSIBLE_NOCOLOR"] = "True"

        # We mount in the utils directory to /opt/ansible_navigator_utils
        # We do this so that we can access key_value_store (KVS) from within
        # the EE. If the Navigator user is overriding PYTHONPATH, we still need
        # to inject this utils directory into the PYTHONPATH. If not, we'll just
        # use the EE's default PYTHONPATH (if it exists) and just add our path
        # at the end.
        if self._args.execution_environment:
            ee_navigator_utils_mount = "/opt/ansible_navigator_utils"
            if "PYTHONPATH" in set_environment_variable:
                set_environment_variable["PYTHONPATH"].append(
                    f":{ee_navigator_utils_mount}",
                )
            else:
                set_environment_variable[
                    "PYTHONPATH"
                ] = f"${{PYTHONPATH}}:{ee_navigator_utils_mount}"
            self._logger.debug(
                "Execution Environment's PYTHONPATH is set to: %s",
                set_environment_variable["PYTHONPATH"],
            )

        kwargs = {
            "container_engine": self._args.container_engine,
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": "interactive",
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_environment_variable,
            "private_data_dir": self._args.ansible_runner_artifact_dir,
            "rotate_artifacts": self._args.ansible_runner_rotate_artifacts_count,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.playbook, str):
            playbook_dir = os.path.dirname(self._args.playbook)
        else:
            playbook_dir = os.getcwd()

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs["container_volume_mounts"] = self._args.execution_environment_volume_mounts

        if isinstance(self._args.container_options, list):
            kwargs["container_options"] = self._args.container_options

        kwargs["host_cwd"] = playbook_dir

        self._adjacent_collection_dir = os.path.join(playbook_dir, "collections")
        cache_path = self._args.internals.cache_path

        pass_through_arg = [
            f"{cache_path}/catalog_collections.py",
            "-a",
            self._adjacent_collection_dir,
            "-c",
            self._collection_cache_path,
        ]

        kwargs["cmdline"] = pass_through_arg

        if self._args.execution_environment:
            self._logger.debug("running collections command with execution environment enabled")
            python_exec_path = "/usr/bin/python3"
            utils_lib = os.path.join(
                os.path.dirname(__file__),
                "..",
                "utils",
            )

            container_volume_mounts = [
                # cache directory which has introspection script
                f"{cache_path}:{cache_path}",
                # KVS library used by both Navigator and the introspection script
                f"{utils_lib}:/opt/ansible_navigator_utils",
            ]
            if os.path.exists(self._adjacent_collection_dir):
                container_volume_mounts.append(
                    f"{self._adjacent_collection_dir}:{self._adjacent_collection_dir}:z",
                )

            mount_doc_cache = True
            # Determine if the doc_cache is relative to the cache directory
            if path_is_relative_to(
                child=Path(self._args.collection_doc_cache_path), parent=(cache_path)
            ):
                mount_doc_cache = False

            # The playbook directory will be mounted as host_cwd, so don't duplicate
            if path_is_relative_to(
                child=Path(self._args.collection_doc_cache_path), parent=(Path(playbook_dir))
            ):
                mount_doc_cache = False

            if mount_doc_cache:
                container_volume_mounts.append(
                    f"{self._args.collection_doc_cache_path}:"
                    f"{self._args.collection_doc_cache_path}:z",
                )

            for volume_mount in container_volume_mounts:
                self._logger.debug("Adding volume mount to container invocation: %s", volume_mount)

            if "container_volume_mounts" in kwargs:
                kwargs["container_volume_mounts"] += container_volume_mounts
            else:
                kwargs["container_volume_mounts"] = container_volume_mounts

        else:
            self._logger.debug("running collections command locally")
            python_exec_path = sys.executable

        self._logger.debug(
            "Invoke runner with executable_cmd: %s and kwargs: %s",
            python_exec_path,
            kwargs,
        )
        _runner = Command(executable_cmd=python_exec_path, **kwargs)
        output, error, ret_code = _runner.run()

        if error:
            msg = f"Error while running catalog collection script: {error}"
            self._logger.error(msg)
        if ret_code:
            self._logger.error(output)
            self.notify_failed()
        if output:
            self._parse(output)

    def _parse(self, output) -> None:
        """Load and process the ``json`` output from the collection cataloging process.

        :param output: The output from the collection cataloging process
        :returns: Nothing
        """
        # pylint: disable=too-many-locals

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
            list(parsed["collections"].values()),
            key=lambda i: i["known_as"],
        )
        volume_mounts = self.app.args.execution_environment_volume_mounts
        if isinstance(volume_mounts, list):
            tmp_list = []
            for mount in volume_mounts:
                source_str, destination_str = mount.split(":")[0:2]
                if not Path(source_str).is_dir():
                    continue
                dest_path = Path(destination_str)
                # /x/ansible_collections/co:/x/ansible_collections/co
                if dest_path.parent.name == "ansible_collections":
                    continue
                # /x/ansible_collections/co/ns:/x/ansible_collections/co/ns
                if dest_path.parent.parent.name == "ansible_collections":
                    continue
                # /x:/x
                if dest_path.name != "ansible_collections":
                    dest_path /= "ansible_collections"
                tmp_list.append(str(dest_path))
            dest_volume_mounts = tuple(tmp_list)
        else:
            dest_volume_mounts = tuple()

        for collection in self._collections:
            collection["__name"] = collection["known_as"]
            collection["__version"] = collection["collection_info"].get("version", "missing")
            collection["__shadowed"] = bool(collection["hidden_by"])
            if self._args.execution_environment:
                if collection["path"].startswith(dest_volume_mounts) or collection[
                    "path"
                ].startswith(self._adjacent_collection_dir):
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

    def _get_collection_plugins_details(self, selected_collection: dict) -> dict:
        """Get plugin details for the given collection.

        :param selected_collection: The selected collection
        :returns: The plugin details like full-name, type and short description.
        """
        plugins_details: dict = {}

        for plugin_checksum, plugin_info in selected_collection["plugin_checksums"].items():
            plugin_type = plugin_info.get("type")
            if plugin_type not in plugins_details:
                plugins_details[plugin_type] = []

            plugin_json = self._collection_cache[plugin_checksum]
            loaded = json.loads(plugin_json)

            plugin = loaded.get("plugin")
            plugin_docs = {}
            plugin_path = os.path.join(
                selected_collection.get("path", ""),
                plugin_info.get("path", ""),
            )
            plugin_docs["path"] = plugin_path
            if plugin and plugin["doc"] is not None:
                try:
                    if "name" in plugin["doc"]:
                        short_name = plugin["doc"]["name"]
                    else:
                        short_name = plugin["doc"][plugin_type]
                except KeyError:
                    short_name = None
                if short_name is None:
                    plugin_docs["full_name"] = selected_collection["known_as"]
                else:
                    plugin_docs["full_name"] = f"{selected_collection['known_as']}.{short_name}"

                if "short_description" in plugin["doc"]:
                    plugin_docs["short_description"] = plugin["doc"]["short_description"]

            plugins_details[plugin_type].append(plugin_docs)

        return plugins_details

    def _parse_collection_info_stdout(self) -> dict:
        # pylint: disable=too-many-nested-blocks
        """Parse collection information from catalog collection cache.

        :returns: The collection information to be displayed on stdout
        """
        collections_info: dict = {
            "collections": [],
        }
        collection_exclude_keys = [
            "file_manifest_file",
            "format",
            "meta_source",
            "plugin_checksums",
            "runtime",
        ]
        roles_exclude_keys = ["readme"]
        self._collection_cache = cast(KeyValueStore, self._collection_cache)

        self._collection_cache.open_()
        for collection in self._collections:
            plugins_details = self._get_collection_plugins_details(collection)

            collection_stdout: dict = {}
            for info_name, info_value in collection.items():
                info_name = remove_dbl_un(info_name)
                if info_name in collection_exclude_keys:
                    continue

                if info_name == "roles":
                    collection_stdout["roles"] = []
                    for role in info_value:
                        updated_role_info = {}
                        for role_info_key, role_info_value in role.items():
                            if role_info_key in roles_exclude_keys:
                                continue
                            updated_role_info[role_info_key] = role_info_value
                        collection_stdout["roles"].append(updated_role_info)
                else:
                    collection_stdout[info_name] = info_value

            collection_stdout["plugins"] = plugins_details
            collections_info["collections"].append(collection_stdout)
        self._collection_cache.close()

        return collections_info
