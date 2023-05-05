"""Inventory subcommand implementation."""
from __future__ import annotations

import glob
import json
import os
import shlex
import shutil

from pathlib import Path
from typing import Any

from ansible_navigator.action_base import ActionBase
from ansible_navigator.action_defs import RunStdoutReturn
from ansible_navigator.app_public import AppPublic
from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.runner import AnsibleInventory
from ansible_navigator.runner import Command
from ansible_navigator.steps import Step
from ansible_navigator.ui_framework import Color
from ansible_navigator.ui_framework import CursesLine
from ansible_navigator.ui_framework import CursesLinePart
from ansible_navigator.ui_framework import CursesLines
from ansible_navigator.ui_framework import Decoration
from ansible_navigator.ui_framework import Interaction
from ansible_navigator.ui_framework import warning_notification

from . import _actions as actions
from . import run_action


def color_menu(colno: int, colname: str, entry: dict[str, Any]) -> tuple[int, int]:
    """Provide a color for a inventory menu entry in one column.

    :param colno: The column number
    :param colname: The column name
    :param entry: The menu entry
    :returns: The color and decoration
    """
    if colname in ["__name", "title", "inventory_hostname"]:
        return Color.BRIGHT_GREEN, Decoration.NORMAL
    if colname == "__taxonomy":
        return Color.BRIGHT_YELLOW, Decoration.NORMAL
    if colname == "description":
        return Color.BRIGHT_BLUE, Decoration.NORMAL
    if colname == "__type":
        if entry["__type"] == "group":
            return Color.BRIGHT_YELLOW, Decoration.NORMAL
        return Color.BRIGHT_BLUE, Decoration.NORMAL
    colors = [
        Color.BRIGHT_CYAN,
        Color.BRIGHT_MAGENTA,
        Color.CYAN,
        Color.MAGENTA,
        Color.BLUE,
        Color.YELLOW,
        Color.GREEN,
    ]
    return colors[colno % len(colors)], Decoration.NORMAL


def content_heading(obj: Any, screen_w: int) -> CursesLines | None:
    """Create a heading for inventory content.

    :param obj: The content going to be shown
    :param screen_w: The current screen width
    :returns: The heading
    """
    host = obj["inventory_hostname"]
    operating_system = obj.get("ansible_network_os", obj.get("ansible_platform", ""))
    string = f"[{host}] {operating_system}"
    string = string + (" " * (screen_w - len(string) + 1))
    line_part = CursesLinePart(
        column=0,
        string=string,
        color=Color.BLACK,
        decoration=Decoration.UNDERLINE,
    )
    return CursesLines((CursesLine((line_part,)),))


def filter_content_keys(obj: dict[Any, Any]) -> dict[Any, Any]:
    """Filter out some keys when showing inventory content.

    :param obj: The object from which keys should be removed
    :returns: The object with keys removed
    """
    return {k: v for k, v in obj.items() if not k.startswith("__")}


class MenuEntry(dict):
    """A menu entry."""


class Menu(list):
    """A menu."""


@actions.register
class Action(ActionBase):
    """Inventory subcommand implementation."""

    # pylint: disable=too-many-instance-attributes

    KEGEX = r"^i(?:nventory)?(\s(?P<params>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:images`` action.

        :param args: The current settings for the application
        """
        super().__init__(args=args, logger_name=__name__, name="inventory")

        self.__inventory: dict[Any, Any] = {}
        self._host_vars: dict[str, dict[Any, Any]]
        self._inventories_mtime: float | None
        self._inventories: list[str] = []
        self._inventory_error: str = ""
        self._runner: Command | AnsibleInventory

    @property
    def _inventory(self) -> dict[Any, Any]:
        """Return the inventory.

        :returns: The inventory details
        """
        return self.__inventory

    @_inventory.setter
    def _inventory(self, value: dict) -> None:
        """Set the inventory and hostvars.

        :param value: The inventory data
        """
        self.__inventory = value
        self._host_vars = {
            k: {**v, "inventory_hostname": k}
            for k, v in value.get("_meta", {}).get("hostvars", {}).items()
        }
        for group in self._inventory:
            for host in self._inventory[group].get("hosts", []):
                if host in self._host_vars:
                    continue
                self._host_vars[host] = {"inventory_hostname": host}

    @property
    def _show_columns(self) -> list:
        """Return the columns to show for an inventory menu.

        :returns: The columns to show
        """
        if isinstance(self._args.inventory_column, list):
            return self._args.inventory_column
        return []

    def _set_inventories_mtime(self) -> None:
        """Record the inventory modification time."""
        modification_times = []
        for inventory in self._inventories:
            if os.path.isdir(inventory):
                modification_times.append(
                    max(
                        os.path.getmtime(e)
                        for e in glob.glob(os.path.join(inventory, "**"), recursive=True)
                    ),
                )
            elif os.path.isfile(inventory):
                modification_times.append(os.path.getmtime(inventory))
        if modification_times:
            self._inventories_mtime = max(modification_times)
        else:
            self._inventories_mtime = None

    def update(self):
        """Request calling app update, inventory update checked in ``run()``."""
        self._calling_app.update()

    def run(self, interaction: Interaction, app: AppPublic) -> Interaction | None:
        """Execute the ``inventory`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: The pending :class:`~ansible_navigator.ui_framework.ui.Interaction` or
            :data:`None`
        """
        self._logger.debug("inventory requested in interactive mode")
        self._prepare_to_run(app, interaction)

        args_updated = self._update_args(
            [self._name] + shlex.split(self._interaction.action.match.groupdict()["params"] or ""),
        )
        if not args_updated:
            self._prepare_to_exit(interaction)
            return None

        self.stdout = self._calling_app.stdout
        self._inventories = self._args.inventory
        self._set_inventories_mtime()

        self._collect_inventory_details()
        if not self._inventory:
            self._prepare_to_exit(interaction)
            return None

        if self._inventory_error:
            while True:
                interaction = self._interaction.ui.show(
                    self._inventory_error,
                    content_format=ContentFormat.ANSI,
                )
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

                self._set_inventories_mtime()

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

    def run_stdout(self) -> RunStdoutReturn:
        """Execute the ``inventory`` request for mode stdout.

        :returns: The return code, 0 or 1. If the runner status if failed, return 1
            along with a message to review the logs.
        """
        self._logger.debug("inventory requested in stdout mode")
        if hasattr(self._args, "inventory") and self._args.inventory:
            self._inventories = self._args.inventory
        self._collect_inventory_details()
        if self._runner.status == "failed":
            return RunStdoutReturn(message="Please review the log for errors.", return_code=1)
        return RunStdoutReturn(message="", return_code=0)

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

    def _build_main_menu(self) -> Step:
        """Build the inventory menu.

        :returns: The inventory menu definition
        """
        groups = MenuEntry(
            title="Browse groups",
            description="Explore each inventory group and group members members",
        )
        hosts = MenuEntry(
            title="Browse hosts",
            description="Explore the inventory with a list of all hosts",
        )

        step = Step(
            name="main_menu",
            columns=["title", "description"],
            select_func=self._step_from_main_menu,
            step_type="menu",
            value=[groups, hosts],
        )
        return step

    def _step_from_main_menu(self) -> Step:
        """Take a step away from the main menu.

        :raises IndexError: When the index does not correspond to a menu entry
        :returns: Either the group or host menu
        """
        if self.steps.current.index == 0:
            return self._build_group_menu("all")
        if self.steps.current.index == 1:
            return self._build_host_menu()
        msg = "broken modules somewhere?"
        raise IndexError(msg)

    def _build_group_menu(self, key=None) -> Step:
        """Build the menu for inventory groups.

        :param key: The optional menu name
        :returns: The inventory group menu definition
        """
        if key is None:
            key = self.steps.current.selected["__name"]

        try:
            menu = Menu()
            taxonomy = "\u25B8".join(
                ["all"]
                + [step.selected["__name"] for step in self.steps if step.name == "group_menu"],
            )

            columns = ["__name", "__taxonomy", "__type"]

            hosts = self._inventory[key].get("hosts", None)
            if hosts:
                columns.extend(self._show_columns)
                for host in sorted(hosts):
                    menu_entry = MenuEntry(**self._host_vars[host])
                    menu_entry["__name"] = menu_entry["inventory_hostname"]
                    menu_entry["__taxonomy"] = taxonomy
                    menu_entry["__type"] = "host"
                    menu.append(menu_entry)

            children = self._inventory[key].get("children", None)
            if children:
                for child in sorted(children):
                    menu_entry = MenuEntry()
                    menu_entry["__name"] = child
                    menu_entry["__taxonomy"] = taxonomy
                    menu_entry["__type"] = "group"
                    if hosts:
                        menu_entry.update({c: "" for c in self._show_columns})
                    menu.append(menu_entry)

            return Step(
                name="group_menu",
                step_type="menu",
                value=menu,
                columns=columns,
                select_func=self._host_or_group_step,
                show_func=self._refresh,
            )
        except KeyError:
            # selected group was removed from inventory
            return self.steps.back_one()

    def _build_host_content(self) -> Step:
        """Build the inventory content for one host.

        :returns: The inventory content for the host
        """
        host_vars = self._host_vars
        try:
            values = [
                host_vars[m_entry.get("__name", m_entry.get("inventory_hostname"))]
                for m_entry in self.steps.current.value
                if "__type" not in m_entry or m_entry["__type"] == "host"
            ]
            entry = Step(
                name="host_content",
                step_type="content",
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
        """Refresh the current step, removing and replacing it."""
        self.steps.back_one()
        self.steps.append(self.steps.current.select_func())

    def _build_host_menu(self) -> Step:
        """Build the menu of hosts.

        :returns: The hosts menu definition
        """
        menu = Menu()
        for host in self._host_vars.values():
            host["__type"] = "host"
            menu.append(MenuEntry(host))
        columns = ["inventory_hostname"] + self._show_columns
        return Step(
            columns=columns,
            name="host_menu",
            step_type="menu",
            value=menu,
            select_func=self._build_host_content,
            show_func=self._refresh,
        )

    def _host_or_group_step(self) -> Step:
        """Build a menu based on the type of the current step.

        :raises TypeError: When the step type is unknown
        :returns: The group or host menu definition
        """
        if self.steps.current.selected["__type"] == "group":
            return self._build_group_menu()
        if self.steps.current.selected["__type"] == "host":
            return self._build_host_content()
        msg = "unknown step type"
        raise TypeError(msg)

    def _collect_inventory_details_interactive(
        self,
        kwargs: dict[str, Any],
    ) -> None:
        """Use the runner subsystem to collect inventory details for mode interactive.

        :param kwargs: The arguments for the runner call
        """
        try:
            # Extract the playbook dir the user may have provided
            index = self._args.cmdline.index("--playbook-dir")
            playbook_dir = self._args.cmdline[index + 1]
            source = "user provided"
        # Constants don't have an index, may go past end of list, param not found
        except (AttributeError, IndexError, ValueError):
            if isinstance(self._args.playbook, str):
                # or use the parent of the currently set playbook
                playbook_dir = str(Path(self._args.playbook).resolve().parent)
                source = "derived from playbook"
            else:
                # or the current working directory
                playbook_dir = os.getcwd()
                source = "CWD"
        self._logger.info("--playbook-directory for inventory from (%s): %s", source, playbook_dir)

        self._runner = AnsibleInventory(**kwargs)
        inventory_output, inventory_err = self._runner.fetch_inventory(
            action="list",
            inventories=self._inventories,
            playbook_dir=playbook_dir,
        )
        if inventory_output:
            parts = inventory_output.split("{", 1)
            inventory_err = parts[0] + inventory_err if inventory_err else parts[0]
            inventory_output = "{" + parts[1] if len(parts) == 2 else ""
        preface = ["Errors were encountered while gathering the inventory:"]
        notify = ("ERROR!", "Error", "Unable to parse")
        if any(string in inventory_err for string in notify):
            if "[WARNING]" in inventory_err:
                parts = inventory_err.split("[WARNING]")
                messages = [part.replace("\n", " ").strip() for part in parts if part]
                present = preface + [f"[WARNING]{message}" for message in messages]
            else:
                present = preface + inventory_err.splitlines()
            for line in present:
                self._logger.error(line)
            warning = warning_notification(present)
            self._interaction.ui.show_form(warning)
        else:
            self._extract_inventory(inventory_output)

    def _collect_inventory_details_automated(
        self,
        kwargs: dict[str, Any],
    ) -> tuple[str | None, str | None, int | None]:
        """Use the runner subsystem to collect inventory details for mode stdout.

        :param kwargs: The arguments for the runner call
        :raises RuntimeError: When the ``ansible-inventory`` command cannot be found for mode stdout
        :returns: The output, errors and return code from runner
        """
        if self._args.execution_environment:
            ansible_inventory_path = "ansible-inventory"
        else:
            exec_path = shutil.which("ansible-inventory")
            if exec_path is None:
                msg = "'ansible-inventory' executable not found"
                self._logger.error(msg)
                raise RuntimeError(msg)

            ansible_inventory_path = exec_path

        pass_through_arg = []
        if self._args.help_inventory is True:
            pass_through_arg.append("--help")

        if isinstance(self._args.cmdline, list):
            pass_through_arg.extend(self._args.cmdline)

        kwargs.update({"cmdline": pass_through_arg, "inventory": self._inventories})

        self._runner = Command(executable_cmd=ansible_inventory_path, **kwargs)
        stdout_return = self._runner.run()
        return stdout_return

    def _collect_inventory_details(
        self,
    ) -> tuple[str | None, str | None, int | None]:
        """Use the runner subsystem to collect inventory details for either mode.

        :returns: For mode interactive nothing. For mode stdout, the output, errors and return
            code from runner
        """
        if isinstance(self._args.set_environment_variable, dict):
            set_env_vars = {**self._args.set_environment_variable}
        else:
            set_env_vars = {}

        if self._args.display_color is False:
            set_env_vars["ANSIBLE_NOCOLOR"] = "1"

        kwargs = {
            "container_engine": self._args.container_engine,
            "host_cwd": os.getcwd(),
            "execution_environment_image": self._args.execution_environment_image,
            "execution_environment": self._args.execution_environment,
            "navigator_mode": self._args.mode,
            "pass_environment_variable": self._args.pass_environment_variable,
            "set_environment_variable": set_env_vars,
            "private_data_dir": self._args.ansible_runner_artifact_dir,
            "rotate_artifacts": self._args.ansible_runner_rotate_artifacts_count,
            "timeout": self._args.ansible_runner_timeout,
        }

        if isinstance(self._args.execution_environment_volume_mounts, list):
            kwargs.update(
                {"container_volume_mounts": self._args.execution_environment_volume_mounts},
            )

        if isinstance(self._args.container_options, list):
            kwargs.update({"container_options": self._args.container_options})

        if self._args.mode == "interactive":
            self._collect_inventory_details_interactive(kwargs)
        else:
            return self._collect_inventory_details_automated(kwargs)

        return (None, None, None)

    def _extract_inventory(self, stdout: str) -> None:
        """Load and the ``json`` output from the inventory collection process.

        :param stdout: The output from the inventory collection process
        """
        try:
            self._inventory = json.loads(stdout)
        except json.JSONDecodeError as exc:
            self._logger.debug("json decode error: %s", str(exc))
            self._logger.debug("tried: %s", stdout)
            self._inventory_error = stdout
