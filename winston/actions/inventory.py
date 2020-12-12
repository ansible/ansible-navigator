""" :inventory """
import curses
import logging
import json
import os
import subprocess

from collections import deque
from distutils.spawn import find_executable
from subprocess import CompletedProcess
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union
from . import _actions as actions
from ..curses_defs import CursesLinePart
from ..curses_defs import CursesLines
from ..ui import Interaction


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> int:
    # pylint: disable=too-many-branches
    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """
    if colname == "__name":
        return 10
    if colname == "__type":
        if entry["__type"] == "group":
            return 11
        return 12
    if colname == "inventory_hostname":
        return 10
    colors = [14, 13, 6, 5, 4, 3, 2]
    return colors[colno % len(colors)]


def color_main_menu(_colno: int, colname: str, _entry: Dict[str, Any]) -> int:
    # pylint: disable=too-many-branches
    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """
    if colname == "title":
        return 10
    if colname == "description":
        return 12
    return 0


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


class Step(NamedTuple):
    """A step in the deque"""

    type: str
    value: Union[Menu, List[Dict]]
    idx: Union[int, None] = None


class Steps(deque):
    """a custom deque"""

    @property
    def adder(self) -> Callable:
        """return self adder"""
        return self._adder

    @adder.setter
    def adder(self, value: Callable) -> None:
        """set the callable used to generate the next step"""
        self._adder = value

    def back_one(self) -> Union[Step, None]:
        """convenience method"""
        if self:
            return self.pop()
        return None

    @property
    def current(self):
        """return the current step"""
        return self[-1]

    def next(self, value: Union[Step, Interaction]) -> None:
        """add the next step to the que"""
        if isinstance(value, Interaction):
            value = self._adder(value)
        self.append(value)


@actions.register
class Action:
    """:inventory"""

    # pylint:disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes

    KEGEX = r"^i(?:nventory)?(\s(?P<inventories>.*))?$"

    def __init__(self):
        self._logger = logging.getLogger()
        self._app: Any
        self.__inventory: Dict[Any, Any]
        self._inventory_error: str = ""
        self._host_vars: Dict[str, Dict[Any, Any]]
        self._steps: Steps = Steps()
        self._steps.adder = self._generate_next_step
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
        return self._app.args.inventory_columns.split(",")

    def run(self, interaction: Interaction, app) -> Union[Interaction, bool]:
        # pylint: disable=too-many-branches
        """Handle :inventory

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("inventory requested")
        self._app = app
        self._interaction = interaction
        self._gererate_inventory()

        if not self._inventory:
            return True

        previous_scroll = interaction.ui.scroll()
        previous_filter = interaction.ui.menu_filter()

        if self._inventory_error:
            self._interaction.ui.show(self._inventory_error, xform="source.ansi")
            interaction.ui.scroll(previous_scroll)
            return True

        groups = MenuEntry(
            title="Browse groups",
            description="Explore each inventory group and group members members",
        )
        hosts = MenuEntry(
            title="Browse hosts", description="Explore the inventory with a list of all hosts"
        )
        while True:
            self._interaction.ui.scroll(0)
            self._interaction.ui.menu_filter(None)

            app.update()

            menu = Menu([groups, hosts])
            result = self._interaction.ui.show(
                obj=menu,
                columns=["title", "description"],
                color_menu_item=color_main_menu,
            )
            if result is True:
                continue
            if result is False or result.action.name == "back":
                break
            if result.action.name == "select":
                if result.action.value == 0:
                    self._explore(self._build_group_menu("all"))
                else:
                    self._explore(self._build_host_menu())

        interaction.ui.scroll(previous_scroll)
        interaction.ui.menu_filter(previous_filter)
        return result

    def _explore(self, initial_step):
        self._steps.clear()
        while True:
            self._app.update()
            self._interaction.ui.scroll(0)

            if not self._steps:
                self._steps.next(initial_step)

            result = self._take_step()

            if isinstance(result, bool):
                self._steps.back_one()
                if result is False:
                    self._steps.back_one()

            elif result.action.name == "refresh":
                if self._steps.current.type == "host_content":
                    step = self._steps.back_one()
                    idx = result.action.value % len(step.value)
                    self._steps.next(step._replace(idx=idx))
                    continue
            elif result.action.name == "select":
                self._steps.next(result)
            elif result.action.name == "back":
                self._steps.back_one()
                if not self._steps:
                    break
            else:
                self._steps.append(result)

    def _build_group_menu(self, key: str) -> Step:
        menu = Menu()
        for host in self._inventory[key].get("hosts", []):
            entry = self._host_vars[host]
            entry["__type"] = "host"
            entry["__name"] = entry["inventory_hostname"]
            menu.append(MenuEntry(entry))
        for child in self._inventory[key].get("children", []):
            menu_entry = MenuEntry(
                __name=child, __type="group", **{c: "" for c in self._show_columns}
            )
            menu.append(menu_entry)
        return Step(type="group_menu", value=menu)

    def _build_host_menu(self) -> Step:
        menu = Menu()
        for host in self._host_vars.values():
            host["__type"] = "host"
            menu.append(MenuEntry(host))
        return Step(type="host_menu", value=menu)

    def _generate_next_step(self, result: Interaction) -> Step:
        value = self._steps.current.value
        idx = result.action.value
        menu_entry = value[idx]
        if menu_entry["__type"] == "group":
            return self._build_group_menu(key=menu_entry["__name"])

        host_vars = self._host_vars
        values = [
            host_vars[m_entry.get("__name", m_entry.get("inventory_hostname"))]
            for m_entry in self._steps.current.value
            if m_entry["__type"] == "host"
        ]
        entry = Step(type="host_content", value=values, idx=int(idx))
        return entry

    def _take_step(self):
        if isinstance(self._steps.current, Interaction):
            result = self._app.actions.run(
                action=self._steps.current.action.name,
                app=self._app,
                interaction=self._steps.current,
            )
        elif isinstance(self._steps.current, Step):
            if self._steps.current.type == "group_menu":
                menu = Menu(self._steps.current.value)
                columns = ["__name", "__type"]
                if "host" in set(t["__type"] for t in menu):
                    columns.extend(self._show_columns)
                result = self._interaction.ui.show(
                    obj=menu,
                    columns=columns,
                    color_menu_item=color_menu,
                )
            elif self._steps.current.type == "host_menu":
                menu = Menu(self._steps.current.value)
                result = self._interaction.ui.show(
                    obj=menu,
                    columns=["inventory_hostname"] + self._show_columns,
                    color_menu_item=color_menu,
                )
            elif self._steps.current.type == "host_content":
                result = self._interaction.ui.show(
                    obj=self._steps.current.value,
                    index=self._steps.current.idx,
                    content_heading=content_heading,
                    filter_content_keys=filter_content_keys,
                )
        return result

    def _gererate_inventory(self) -> None:
        if inventories := self._interaction.action.match.groupdict()["inventories"]:
            inventories = [os.path.abspath(i) for i in inventories.split(",")]
            self._logger.debug("inventories set by user: %s", inventories)
        elif hasattr(self._app.args, "inventory") and (inventories := self._app.args.inventory):
            self._logger.info("no inventory provided, using inventory from args")
        else:
            return

        if self._app.args.execution_environment:
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
        cmd = [self._app.args.container_engine, "run", "-i", "-t"]

        for inventory_path in inventory_paths:
            cmd.extend(["-v", f"{inventory_path}:{inventory_path}"])

        cmd.extend([self._app.args.ee_image])
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
