""" :doc """
import curses
import logging
import os
import re
import subprocess

from argparse import Namespace
from distutils.spawn import find_executable

from typing import Any
from typing import Dict
from typing import List
from typing import Union

from . import run as run_action
from . import _actions as actions
from ..app import App
from ..app_public import AppPublic
from ..steps import Step

from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction

from ..yaml import yaml
from ..yaml import Loader


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=unused-argument

    """color the menu"""
    if entry["__default"] is False:
        return 3
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
    string = obj["option"].replace("_", " ")
    if obj["__default"] is False:
        string += f" (current: {obj['__current_value']})  (default: {obj['default']})"
        color = 3
    else:
        string += f" (current/default: {obj['__current_value']})"
        color = 2

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


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    return {k: v for k, v in obj.items() if not k.startswith("__")}


@actions.register
class Action(App):
    """:doc"""

    # pylint:disable=too-few-public-methods

    KEGEX = r"^config$"

    def __init__(self, args):
        super().__init__(args=args)
        self._args = args
        self._interaction: Interaction
        self._logger = logging.getLogger(__name__)
        self._app = None
        self._config = None

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :doc

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("config requested")
        self._app = app
        self._interaction = interaction

        if app.args.execution_environment:
            self._logger.debug("trying execution environment")
            self._try_ee(app.args)

        if self._config is None:
            self._logger.debug("trying local")
            self._try_local(app.args)

        if self._config is None:
            return None

        self.steps.append(self._build_main_menu())
        previous_scroll = interaction.ui.scroll()
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
        return Step(
            name="all_options",
            columns=["option", "__default", "source", "via", "__current_value"],
            select_func=self._build_option_content,
            tipe="menu",
            value=self._config,
        )

    def _build_option_content(self):
        """build the content for one option"""
        return Step(
            name="option_content",
            tipe="content",
            value=self._config,
            index=self.steps.current.index,
        )

    def _try_ee(self, args: Namespace) -> None:
        """run config in ee"""
        if "playbook" in self._app.args:
            playbook_dir = os.path.dirname(args.playbook)
        else:
            playbook_dir = os.getcwd()

        cmd = [args.container_engine, "run", "-i", "-t"]
        cmd.extend(["--env", "ANSIBLE_NOCOLOR=True"])
        cmd.extend(["-v", "{pdir}:{pdir}".format(pdir=playbook_dir)])
        cmd.extend([args.ee_image])
        cmd.extend(["cd", playbook_dir, "&&", "ansible-config"])

        list_cmd = cmd + ["list"]
        dump_cmd = cmd + ["dump"]

        self._logger.debug("ee list command: %s", " ".join(list_cmd))
        self._logger.debug("ee dump command: %s", " ".join(dump_cmd))

        self._dispatch(list_cmd, dump_cmd)

    def _try_local(self, args: Namespace) -> None:
        """run config locally"""
        aconfig_path = find_executable("ansible-config")
        if aconfig_path:
            if "playbook" in self._app.args:
                playbook_dir = os.path.dirname(args.playbook)
            else:
                playbook_dir = os.getcwd()

            self._logger.debug("local ansible-config path is: %s", aconfig_path)
            cmd = ["cd", playbook_dir, "&&", aconfig_path]
            list_cmd = cmd + ["list"]
            dump_cmd = cmd + ["dump"]

            self._logger.debug("local list command: %s", " ".join(list_cmd))
            self._logger.debug("local dump command: %s", " ".join(dump_cmd))

            self._dispatch(list_cmd, dump_cmd)
            return

        msg = "no ansible-config command found in path"
        self._logger.error(msg)
        return

    def _dispatch(self, list_cmd: List[str], dump_cmd: List[str]) -> None:
        """run the individual config commands and parse"""
        list_output = self._run_command(list_cmd)
        if list_output is None:
            return None
        dump_output = self._run_command(dump_cmd)
        if dump_output is None:
            return None
        self._parse_and_merge(list_output, dump_output)
        return None

    def _run_command(self, cmd) -> Union[None, subprocess.CompletedProcess]:
        """run a command"""
        try:
            proc_out = subprocess.run(
                " ".join(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                universal_newlines=True,
                shell=True,
            )
            self._logger.debug(
                "ansible-config output %s", proc_out.stdout[0:100].replace("\n", " ") + "<...>"
            )
            return proc_out

        except subprocess.CalledProcessError as exc:
            self._logger.debug("command execution failed: '%s'", str(exc))
            self._logger.debug("command execution failed: '%s'", exc.output)
            return None

    def _parse_and_merge(self, list_output, dump_output) -> None:
        """yaml load the list, and parse the dump
        merge dump int list
        """
        # pylint: disable=too-many-branches
        try:
            parsed = yaml.load(list_output.stdout, Loader=Loader)
            self._logger.debug("yaml loading list output succeeded")
        except yaml.YAMLError as exc:
            self._logger.debug("error yaml loading list output: '%s'", str(exc))
            return None

        regex = re.compile(r"^(?P<variable>\S+)\((?P<source>.*)\)\s=\s(?P<current>.*)$")
        for line in dump_output.stdout.splitlines():
            extracted = regex.match(line)
            if extracted:
                variable = extracted.groupdict()["variable"]
                try:
                    source = yaml.load(extracted.groupdict()["source"], Loader=Loader)
                except yaml.YAMLError as exc:
                    source = extracted.groupdict()["source"]
                try:
                    current = yaml.load(extracted.groupdict()["current"], Loader=Loader)
                except yaml.YAMLError as exc:
                    current = extracted.groupdict()["current"]
                try:
                    if isinstance(source, dict):
                        parsed[variable]["source"] = list(source.keys())[0]
                        parsed[variable]["via"] = list(source.values())[0]
                    else:
                        parsed[variable]["source"] = source
                        parsed[variable]["via"] = source
                    parsed[variable]["current"] = current
                    parsed[variable]["__current_value"] = extracted.groupdict()["current"]
                except KeyError as exc:
                    self._logger.error("variable '%s' not found in list output")
                    return None
            else:
                self._logger.error("Unparsable dump entry: %s", line)
                return None

        for key, value in parsed.items():
            value["option"] = key
            if value["source"] == "default":
                value["__default"] = True
            else:
                value["__default"] = False

        self._config = list(parsed.values())
        self._logger.debug("parsed and merged list and dump sucessfully")
        return None
