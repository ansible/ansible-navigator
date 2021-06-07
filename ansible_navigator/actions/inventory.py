""" :inventory """
import curses
import glob
import json
import os
import shlex
import shutil

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
from ..runner.api import CommandRunner, InventoryRunner
from ..steps import Step
from ..ui_framework import CursesLinePart
from ..ui_framework import CursesLines
from ..ui_framework import Interaction
from ..ui_framework import dict_to_form
from ..ui_framework import warning_notification


def color_menu(colno: int, colname: str, entry: Dict[str, Any]) -> Tuple[int, int]:
    """Find matching color for word

    :param word: A word to match
    :type word: str(able)
    """
    if colname in ["__name", "title", "inventory_hostname"]:
        return 10, 0
    if colname == "__taxonomy":
        return 11, 0
    if colname == "description":
        return 12, 0
    if colname == "__type":
        if entry["__type"] == "group":
            return 11, 0
        return 12, 0
    colors = [14, 13, 6, 5, 4, 3, 2]
    return colors[colno % len(colors)], 0


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
                    color=0,
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

    KEGEX = r"^i(?:nventory)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        super().__init__(args=args, logger_name=__name__, name="inventory")

        self.__inventory: Dict[Any, Any] = {}
        self._host_vars: Dict[str, Dict[Any, Any]]
        self._inventories_mtime: float
        self._inventories: List[str] = []
        self._inventory_error: str = ""
        self._runner: Union[CommandRunner, InventoryRunner]

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
    def _show_columns(self) -> List:
        if isinstance(self._args.inventory_column, list):
            return self._args.inventory_column
        return []

    def _set_inventories_mtime(self) -> None:
        mtimes = []
        for inventory in self._inventories:
            if os.path.isdir(inventory):
                mtimes.append(
                    max(
                        (
                            os.path.getmtime(e)
                            for e in glob.glob(os.path.join(inventory, "**"), recursive=True)
                        )
                    )
                )
            elif os.path.isfile(inventory):
                mtimes.append(os.path.getmtime(inventory))
        self._inventories_mtime = max(mtimes)

    def update(self):
        self._calling_app.update()

    def run(self, interaction: Interaction, app: AppPublic) -> Union[Interaction, None]:
        # pylint: disable=too-many-branches
        """Handle :inventory

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param calling_app: The calling_app instance
        :type calling_app: App
        """
        self._logger.debug("inventory requested in interactive mode")
        self._prepare_to_run(app, interaction)
        self.stdout = self._calling_app.stdout

        self._build_inventory_list()
        if not self._inventories:
            self._prepare_to_exit(interaction)
            return None

        self._collect_inventory_details()
        if not self._inventory:
            self._prepare_to_exit(interaction)
            return None

        if self._inventory_error:
            while True:
                interaction = self._interaction.ui.show(self._inventory_error, xform="source.ansi")
                if interaction.name != "refresh":
                    break
            self._prepare_to_exit(interaction)
            return None

        self.steps.append(self._build_main_menu())

        while True:
            self.update()
            self._take_step()
            if not self.steps:
                break

            current_mtime = self._inventories_mtime
            self._set_inventories_mtime()
            if current_mtime != self._inventories_mtime:
                self._logger.debug("inventory changed")

                self._build_inventory_list()
                if not self._inventories:
                    break

                self._collect_inventory_details()
                if not self._inventory:
                    break

                if self._inventory_error:
                    self._logger.error(self._inventory_error)
                    break

            if self.steps.current.name == "quit":
                return self.steps.current

        self._prepare_to_exit(interaction)
        return None

    def run_stdout(self) -> int:
        """Run in oldschool mode, just stdout"""
        self._logger.debug("inventory requested in stdout mode")
        if hasattr(self._args, "inventory") and self._args.inventory:
            self._inventories = self._args.inventory
        self._collect_inventory_details()
        return 1 if self._runner.status == "failed" else 0

    def _take_step(self) -> None:

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

    def _build_main_menu(self) -> Step:
        groups = MenuEntry(
            title="Browse groups",
            description="Explore each inventory group and group members members",
        )
        hosts = MenuEntry(
            title="Browse hosts", description="Explore the inventory with a list of all hosts"
        )

        step = Step(
            name="main_menu",
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

        try:

            menu = Menu()
            taxonomy = "\u25B8".join(
                ["all"]
                + [step.selected["__name"] for step in self.steps if step.name == "group_menu"]
            )

            columns = ["__name", "__taxonomy", "__type"]

            hosts = self._inventory[key].get("hosts", None)
            if hosts:
                columns.extend(self._show_columns)
                for host in hosts:
                    menu_entry = MenuEntry(**self._host_vars[host])
                    menu_entry["__name"] = menu_entry["inventory_hostname"]
                    menu_entry["__taxonomy"] = taxonomy
                    menu_entry["__type"] = "host"
                    menu.append(menu_entry)

            children = self._inventory[key].get("children", None)
            if children:
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
                show_func=self._refresh,
            )
        except KeyError:
            # selected group was removed from inventory
            return self.steps.back_one()

    def _build_host_content(self) -> Step:
        host_vars = self._host_vars
        try:
            values = [
                host_vars[m_entry.get("__name", m_entry.get("inventory_hostname"))]
                for m_entry in self.steps.current.value
                if "__type" not in m_entry or m_entry["__type"] == "host"
            ]
            entry = Step(
                name="host_content",
                tipe="content",
                value=values,
                index=self.steps.current.index,
                columns=["__name"] + self._show_columns,
                show_func=self._refresh,
            )
            return entry
        except KeyError:
            # selected host removed from inventory
            return self.steps.back_one()

    def _refresh(self) -> None:
        """rebuild the current step and replace"""
        self.steps.back_one()
        self.steps.append(self.steps.current.select_func())

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
            show_func=self._refresh,
        )

    def _host_or_group_step(self) -> Step:
        if self.steps.current.selected["__type"] == "group":
            return self._build_group_menu()
        if self.steps.current.selected["__type"] == "host":
            return self._build_host_content()
        raise TypeError("unknown step type")

    def _build_inventory_list(self) -> None:

        self._update_args(
            [self._name] + shlex.split(self._interaction.action.match.groupdict()["params"] or "")
        )

        if isinstance(self._args.inventory, list):
            inventories = self._args.inventory
            inventories_valid = all((os.path.exists(inv) for inv in inventories))
        else:
            inventories = ["", "", ""]
            inventories_valid = False

        if not inventories_valid:
            FType = Dict[str, Any]
            form_dict: FType = {
                "title": "One or more inventory sources could not be found",
                "fields": [],
            }
            if inventories:
                for idx, inv in enumerate(inventories):
                    form_field = {
                        "name": f"inv_{idx}",
                        "pre_populate": inv,
                        "prompt": f"{idx}. Inventory source",
                        "type": "text_input",
                        "validator": {"name": "valid_path_or_none"},
                    }
                    form_dict["fields"].append(form_field)
            else:
                form_field = {
                    "name": "inv_0",
                    "prompt": "0. Inventory source",
                    "type": "text_input",
                    "validator": {"name": "valid_path_or_none"},
                }
                form_dict["fields"].append(form_field)

            form = dict_to_form(form_dict)
            self._interaction.ui.show(form)

            if form.cancelled:
                return

            inventories = [
                field.value
                for field in form.fields
                if hasattr(field, "value") and field.value != ""
            ]
            if not inventories:
                return

        self._inventories = inventories
        self._set_inventories_mtime()
        return

    def _collect_inventory_details(self) -> None:

        # pylint:disable=too-many-branches

        if isinstance(self._args.set_environment_variable, dict):
            set_envvars = {**self._args.set_environment_variable}
        else:
            set_envvars = {}

        if self._args.display_color is False:
            set_envvars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_envvars,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts}
            )

        if self._args.mode == "interactive":
            self._runner = InventoryRunner(**kwargs)
            inventory_output, inventory_err = self._runner.fetch_inventory(
                "list", self._inventories
            )
            if inventory_output:
                parts = inventory_output.split("{", 1)
                if inventory_err:
                    inventory_err = parts[0] + inventory_err
                else:
                    inventory_err = parts[0]

                if len(parts) == 2:
                    inventory_output = "{" + parts[1]
                else:
                    inventory_output = ""
            warn_msg = ["Errors were encountered while gathering the inventory:"]
            warn_msg += inventory_err.splitlines()
            self._logger.error(" ".join(warn_msg))
            if "Error" in inventory_err:
                warning = warning_notification(warn_msg)
                self._interaction.ui.show(warning)
                return

            self._extract_inventory(inventory_output, inventory_err)
        else:
            if self._args.execution_environment:
                ansible_inventory_path = "ansible-inventory"
            else:
                exec_path = shutil.which("ansible-inventory")
                if exec_path is None:
                    self._logger.error("no ansible-inventory command found in path")
                    return
                ansible_inventory_path = exec_path

            pass_through_arg = []
            if self._args.help_inventory is True:
                pass_through_arg.append("--help")

            if isinstance(self._args.cmdline, list):
                pass_through_arg.extend(self._args.cmdline)

            kwargs.update({"cmdline": pass_through_arg, "inventory": self._inventories})

            self._runner = CommandRunner(executable_cmd=ansible_inventory_path, **kwargs)
            self._runner.run()

    def _extract_inventory(self, stdout: str, stderr: str) -> None:
        try:
            self._inventory = json.loads(stdout)
            if not self._host_vars:
                self._inventory_error = stderr

        except json.JSONDecodeError as exc:
            self._logger.debug("json decode error: %s", str(exc))
            self._logger.debug("tried: %s", stdout)
            self._inventory_error = stdout
