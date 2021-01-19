""" :doc """
import curses
import json
import logging
import os
import subprocess

from argparse import Namespace
from json.decoder import JSONDecodeError

from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from . import run as run_action
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..steps import Step

from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=unused-argument

    """color the menu"""
    if entry.get("__shadowed") is True:
        return 8
    if entry.get("__deprecated") is True:
        return 9
    return 2


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
                    color=curses.color_pair(2),
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

    def __init__(self, args):
        super().__init__(args=args)
        self._args: Namespace
        self._interaction: Interaction
        self._logger = logging.getLogger(__name__)
        self._app = None
        self._collections: List = []
        self._stats: Dict = {}
        self._collection_cache = args.collection_doc_cache
        self._collection_cache_path = args.collection_doc_cache.path
        self._adjacent_collection_dir: str
        self._parser_error: str = ""

    
    def parser_error(self, message: str) -> Tuple[None, None]:
        """callback for parser error

        :param message: A message from the parser
        :type message: str
        """
        self._parser_error = message
        return None, None

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("collections requested")
        self._app = app
        self._interaction = interaction

        previous_scroll = interaction.ui.scroll()
        interaction.ui.scroll(0)
        interaction.ui.show(
            obj="Collecting collection content, this may take a minute the first time...",
            xform="text",
            await_input=False,
        )

        if provided_params := interaction.action.match.groupdict()["params"]:
            self._logger.debug("Parsing provide params: %s", provided_params)
            params = f"collections {provided_params}".split()
            messages, self._args = self.app.args.parse_and_update(
                params=params, error_cb=self.parser_error
            )
            # assume this is params provided
            self._args.execution_environment = True
            for message in messages:
                self._logger.debug(message)
            if self._parser_error:
                self._logger.error(self._parser_error)
                return None
        else:
            self._args = self._app.args
           


        if self._args.execution_environment:
            self._logger.debug("running execution environment")
            self._try_ee()
        else:
            self._logger.debug("running local")
            self._try_local()

        if not self._collections:
            interaction.ui.scroll(previous_scroll)
            return None

        self.steps.append(self._build_main_menu())
        previous_filter = interaction.ui.menu_filter()
        interaction.ui.scroll(0)

        while True:
            self._app.update()
            self._take_step()

            if not self.steps:
                break

            if self.steps.current.name == "quit":
                return self.steps.current

        interaction.ui.scroll(previous_scroll)
        interaction.ui.menu_filter(previous_filter)
        return None

    def _take_step(self) -> None:
        """take one step"""
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
                result = self._interaction.ui.show(
                    obj=self.steps.current.value,
                    columns=self.steps.current.columns,
                    color_menu_item=color_menu,
                    distribution="sacrifice",
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
            columns=["__name", "__version", "__shadowed", "__type", "path"]
        else:
            columns=["__name", "__version", "__shadowed", "path"]

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
            columns=[
                cname_col,
                "__type",
                "__added",
                "__deprecated",
                "__description",
            ],
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

    def _try_ee(self) -> None:
        """run collection catalog in ee"""
        if "playbook" in self._args:
            playbook_dir = os.path.dirname(self._args.playbook)
        else:
            playbook_dir = os.getcwd()

        self._adjacent_collection_dir = playbook_dir + "/collections"

        cmd = [self._args.container_engine, "run", "-i", "-t"]

        cmd += ["-v", f"{self._args.share_dir}/utils:{self._args.share_dir}/utils:z"]

        if os.path.exists(self._adjacent_collection_dir):
            cmd += ["-v", f"{self._adjacent_collection_dir}:{self._adjacent_collection_dir}:z"]

        cmd += [
            "-v",
            f"{self._collection_cache_path}:{self._collection_cache_path}:z",
        ]

        cmd += [self._args.ee_image]
        cmd += ["python3", f"{self._args.share_dir}/utils/catalog_collections.py"]
        cmd += ["-a", self._adjacent_collection_dir]
        cmd += ["-c", self._collection_cache_path]

        self._logger.debug("ee command: %s", " ".join(cmd))
        self._dispatch(cmd)

    def _try_local(self, args: Namespace) -> None:
        """run config locally"""
        if "playbook" in self._args:
            playbook_dir = os.path.dirname(args.playbook)
        else:
            playbook_dir = os.getcwd()

        adjacent_collection_dir = playbook_dir + "/collections"

        cmd = ["python3", f"{args.share_dir}/utils/catalog_collections.py"]
        cmd += ["-a", adjacent_collection_dir]
        cmd += ["-c", self._collection_cache_path]
        self._logger.debug("local command: %s", " ".join(cmd))
        self._dispatch(cmd)

    def _dispatch(self, cmd: List[str]) -> None:
        """run the individual config commands and parse"""
        output = self._run_command(cmd)
        if output is None:
            return None
        self._parse(output)
        return None

    def _run_command(self, cmd) -> Union[None, subprocess.CompletedProcess]:
        """run a command"""
        try:
            proc_out = subprocess.run(
                " ".join(cmd), capture_output=True, check=True, text=True, shell=True
            )
            self._logger.debug("cmd output %s", proc_out.stdout[0:100].replace("\n", " ") + "<...>")
            return proc_out

        except subprocess.CalledProcessError as exc:
            self._logger.debug("command execution failed: '%s'", str(exc))
            self._logger.debug("command execution failed: '%s'", exc.output)
            self._logger.debug("command execution failed: '%s'", exc.stderr)
            return None

    def _parse(self, output) -> None:
        """yaml load the list, and parse the dump
        merge dump int list
        """
        # pylint: disable=too-many-branches
        try:
            if not output.stdout.startswith("{"):
                _warnings, json_str = output.stdout.split("{", 1)
                json_str = "{" + json_str
            else:
                json_str = output.stdout
            parsed = json.loads(json_str)
            self._logger.debug("json loading output succeeded")
        except (JSONDecodeError, ValueError) as exc:
            self._logger.error("Unable to extract collection json from stdout")
            self._logger.debug("error json loading output: '%s'", str(exc))
            self._logger.debug(output.stdout)
            return None

        for error in parsed["errors"]:
            self._logger.error("%s %s", error["path"], error["error"])

        self._collections = sorted(
            list(parsed["collections"].values()), key=lambda i: i["known_as"]
        )
        for collection in self._collections:
            collection["__name"] = collection["known_as"]
            collection["__version"] = collection["collection_info"]["version"]
            collection["__shadowed"] = bool(collection["hidden_by"])
            if self._args.execution_environment:
                if collection['path'].startswith(self._adjacent_collection_dir):
                    collection['__type'] = "bind_mount"
                else:
                    collection['__type'] = "contained"

        self._stats = parsed["stats"]

        for stat, value in self._stats.items():
            self._logger.debug("%s: %s", stat, value)
        return None
