""" :inventory """
import curses
import logging
import json
import os
import subprocess

from distutils.spawn import find_executable
from subprocess import CompletedProcess
from typing import Any
from typing import Dict
from typing import List
from typing import Union
from . import _actions as actions
from ..app import App
from ..curses_defs import CursesLinePart
from ..curses_defs import CursesLines
from ..steps import Step
from ..ui import Interaction


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """
    if colname in ["__name", "title", "inventory_hostname"]:
        return 10
    if colname == "__taxonomy":
        return 11
    if colname == "description":
        return 12
    if colname == "__type":
        if entry["__type"] == "group":
            return 11
        return 12
    colors = [14, 13, 6, 5, 4, 3, 2]
    return colors[colno % len(colors)]


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
    string = "[{host}] {os}".format(
        host=obj["inventory_hostname"],
        os=obj.get("ansible_network_os", obj.get("ansible_platform", "")),
    )
    string = string + (" " * (screen_w - len(string) + 1))
    heading.append(
        tuple(
            [
                CursesLinePart(
                    column=0,
                    string=string,
                    color=curses.color_pair(0),
                    decoration=curses.A_UNDERLINE,
                )
            ]
        )
    )
    return tuple(heading)


def filter_content_keys(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    """when showing content, filter out some keys"""
    return {k: v for k, v in obj.items() if not k.startswith("__")}


class MenuEntry(dict):
    """a menu entry"""


class Menu(list):
    """a menu"""


@actions.register
class Action(App):
    """:inventory"""

    # pylint:disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes

    KEGEX = r"^i(?:nventory)?(\s(?P<inventories>.*))?$"

    def __init__(self):
        super().__init__()
        self._calling_app: App
        self._logger = logging.getLogger(__name__)
        self.__inventory: Dict[Any, Any] = {}
        self._inventory_error: str = ""
        self._host_vars: Dict[str, Dict[Any, Any]]
        self.name = "inventory"
        self._interaction: Interaction

    @property
    def _inventory(self) -> Dict[Any, Any]:
        """return the inventory"""
        return self.__inventory

    @_inventory.setter
    def _inventory(self, value: Dict) -> None:
        """set the inventory
        and hostvars
        """
        self.__inventory = value
        self._host_vars = {
            k: {**v, "inventory_hostname": k}
            for k, v in value.get("_meta", {}).get("hostvars", {}).items()
        }

    @property
    def _show_columns(self):
        return self.args.inventory_columns.split(",")

    def run(self, interaction: Interaction, app) -> None:
        # pylint: disable=too-many-branches
        """Handle :inventory

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("inventory requested")
        self._calling_app = app
        self.args = app.args
        self.stdout = app.stdout
        self._interaction = interaction
        self._generate_inventory()

        if not self._inventory:
            return None

        previous_scroll = interaction.ui.scroll()
        previous_filter = interaction.ui.menu_filter()

        if self._inventory_error:
            self._interaction.ui.show(self._inventory_error, xform="source.ansi")
            interaction.ui.scroll(previous_scroll)
            return None

        self.steps.clear()
        self.steps.append(self._build_main_menu())
        self._interaction.ui.scroll(0)
        while True:
            self._calling_app.update()
            self._take_step()

            if not self.steps:
                if self.args.app == self.name:
                    self.steps.append(self._build_main_menu())
                else:
                    break

            if self.steps.current.name == "quit":
                return self.steps.current

        interaction.ui.scroll(previous_scroll)
        interaction.ui.menu_filter(previous_filter)
        return None

    def _take_step(self) -> None:
        if isinstance(self.steps.current, Interaction):
            result = self.actions.run(
                action=self.steps.current.name,
                app=self,
                interaction=self.steps.current,
            )
        elif isinstance(self.steps.current, Step):
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

    def _build_main_menu(self) -> Step:
        groups = MenuEntry(
            title="Browse groups",
            description="Explore each inventory group and group members members",
        )
        hosts = MenuEntry(
            title="Browse hosts", description="Explore the inventory with a list of all hosts"
        )

        step = Step(
            columns=["title", "description"],
            select_func=self._step_from_main_menu,
            tipe="menu",
            value=[groups, hosts],
        )
        return step

    def _step_from_main_menu(self) -> Step:
        if self.steps.current.index == 0:
            return self._build_group_menu("all")
        if self.steps.current.index == 1:
            return self._build_host_menu()
        raise IndexError("broken modules somewhere?")

    def _build_group_menu(self, key=None) -> Step:
        if key is None:
            key = self.steps.current.selected["__name"]

        menu = Menu()
        taxonomy = "\u25B8".join(
            ["all"] + [step.selected["__name"] for step in self.steps if step.name == "group_menu"]
        )

        columns = ["__name", "__taxonomy", "__type"]

        if hosts := self._inventory[key].get("hosts", None):
            columns.extend(self._show_columns)
            for host in hosts:
                menu_entry = MenuEntry(**self._host_vars[host])
                menu_entry["__name"] = menu_entry["inventory_hostname"]
                menu_entry["__taxonomy"] = taxonomy
                menu_entry["__type"] = "host"
                menu.append(menu_entry)

        if children := self._inventory[key].get("children", None):
            for child in children:
                menu_entry = MenuEntry()
                menu_entry["__name"] = child
                menu_entry["__taxonomy"] = taxonomy
                menu_entry["__type"] = "group"
                if hosts:
                    menu_entry.update({c: "" for c in self._show_columns})
                menu.append(menu_entry)

        return Step(
            name="group_menu",
            tipe="menu",
            value=menu,
            columns=columns,
            select_func=self._host_or_group_step,
        )

    def _build_host_content(self) -> Step:
        host_vars = self._host_vars
        values = [
            host_vars[m_entry.get("__name", m_entry.get("inventory_hostname"))]
            for m_entry in self.steps.current.value
            if m_entry["__type"] == "host"
        ]
        entry = Step(
            name="host_content",
            tipe="content",
            value=values,
            index=self.steps.current.index,
            columns=["__name"] + self._show_columns,
        )
        return entry

    def _build_host_menu(self) -> Step:
        menu = Menu()
        for host in self._host_vars.values():
            host["__type"] = "host"
            menu.append(MenuEntry(host))
        columns = ["inventory_hostname"] + self._show_columns
        return Step(
            columns=columns,
            name="host_menu",
            tipe="menu",
            value=menu,
            select_func=self._build_host_content,
        )

    def _host_or_group_step(self) -> Step:
        if self.steps.current.selected["__type"] == "group":
            return self._build_group_menu()
        if self.steps.current.selected["__type"] == "host":
            return self._build_host_content()
        raise TypeError("unknown step type")

    def _generate_inventory(self) -> None:
        if inventories := self._interaction.action.match.groupdict()["inventories"]:
            inventories = [os.path.abspath(i) for i in inventories.split(",")]
            self._logger.debug("inventories set by user: %s", inventories)
        elif hasattr(self.args, "inventory") and (inventories := self.args.inventory):
            self._logger.info("no inventory provided, using inventory from args")
        else:
            self._logger.error("no inventory set at command line or requested")
            return

        if self.args.execution_environment:
            self._logger.debug("trying execution environment")
            self._try_ee(inventories)
        else:
            self._logger.debug("trying local")
            self._try_local(inventories)

    @staticmethod
    def _inventory_cmdline(
        inventories: List[str], executable: str = "ansible-inventory"
    ) -> List[str]:
        cmd = [executable]
        for inventory in inventories:
            cmd.extend(["-i", inventory])
        cmd.extend(["--list"])
        return cmd

    def _try_ee(self, inventories: List[str]) -> None:
        inventory_paths = (os.path.dirname(i) for i in inventories)
        cmd = [self.args.container_engine, "run", "-i", "-t"]

        for inventory_path in inventory_paths:
            cmd.extend(["-v", f"{inventory_path}:{inventory_path}"])

        cmd.extend([self.args.ee_image])
        cmd.extend(self._inventory_cmdline(inventories))

        cmdline = " ".join(cmd)
        self._logger.debug("running: %s", cmdline)
        result = self._run_command(cmdline)
        if result:
            parts = result.stdout.split("{", 1)
            stderr = parts[0]

            if len(parts) == 2:
                stdout = "{" + parts[1]
            else:
                stdout = ""
            self._extract_inventory(stdout, stderr)

    def _try_local(self, inventories: List[str]) -> None:
        icmd_path = find_executable("ansible-inventory")
        if not icmd_path:
            msg = "no ansible-inventory command found in path"
            self._logger.error(msg)
            self._inventory_error = msg
            return

        cmd = self._inventory_cmdline(inventories, executable=icmd_path)
        cmdline = " ".join(cmd)
        self._logger.debug("running: %s", cmd)
        result = self._run_command(cmdline)
        if result:
            self._extract_inventory(result.stdout, result.stderr)

    def _extract_inventory(self, stdout: str, stderr: str) -> None:
        try:
            self._inventory = json.loads(stdout)
            if not self._host_vars:
                self._inventory_error = stderr

        except json.JSONDecodeError as exc:
            self._logger.debug("json decode error: %s", str(exc))
            self._logger.debug("tried: %s", stdout)
            self._inventory_error = stdout

    def _run_command(self, cmdline: str) -> Union[CompletedProcess, None]:
        try:
            proc_out = subprocess.run(
                cmdline, capture_output=True, check=True, text=True, shell=True
            )
            return proc_out

        except subprocess.CalledProcessError as exc:
            self._logger.debug("command execution failed: '%s'", str(exc))
            self._logger.debug("command execution failed: '%s'", exc.output)
            self._inventory_error = exc.output
            return None
