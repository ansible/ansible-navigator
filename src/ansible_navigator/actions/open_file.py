"""``:open`` command implementation."""
import curses
import json
import logging
import os
import tempfile

from typing import Any
from typing import Callable
from typing import Dict
from typing import List

from .._yaml import human_dump
from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction
from ..ui_framework import Menu
from ..utils import remove_dbl_un
from . import _actions as actions


class SuspendCurses:
    """Context Manager to temporarily leave curses mode."""

    def __enter__(self):
        """Close the curses window."""
        curses.endwin()

    def __exit__(self, exc_type, exc_val, traceback):
        """Open the curses window.

        :param exc_type: The exception class
        :param exc_val: The type of exception
        :param traceback: Report of all information related to the exception
        """
        newscr = curses.initscr()
        newscr.refresh()
        curses.doupdate()


@actions.register
class Action:
    """``:open`` command implementation."""

    KEGEX = r"^o(?:pen)?(\s(?P<something>.*))?$"

    def __init__(self, args: ApplicationConfiguration):
        """Initialize the ``:open`` action.

        :param args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def _menu(self, menu: Menu, menu_filter: Callable) -> List[Dict[Any, Any]]:
        """Convert a menu into structured data.

        :param menu: The current menu showing
        :param menu_filter: The effective menu filter
        :returns: The menu converted to a structured data
        """
        self._logger.debug("menu is showing, open that")
        obj = [
            {remove_dbl_un(k): v for k, v in c.items() if k in menu.columns} for c in menu.current
        ]
        if menu_filter():
            obj = [e for e in obj if menu_filter().search(" ".join(str(v) for v in e.values()))]
        return obj

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        # pylint: disable=too-many-branches
        # pylint: disable=unused-argument
        """Execute the ``:open`` request for mode interactive.

        :param interaction: The interaction from the user
        :param app: The app instance
        :returns: Nothing
        """
        self._logger.debug("open requested")

        filename = None
        line_number = 0

        something = interaction.action.match.groupdict()["something"]
        if something:
            parts = something.rsplit(":", 1)
            if os.path.isfile(parts[0]):
                filename = parts[0]
                line_number = parts[1:][0] if parts[1:] else 0
            else:
                obj = something
        else:
            if interaction.content:
                obj = interaction.content.showing
            elif interaction.menu:
                obj = self._menu(menu=interaction.menu, menu_filter=interaction.ui.menu_filter)
            else:
                return None

        if not filename:
            if interaction.ui.serialization_format() == "text.html.markdown":
                with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_file:
                    filename = temp_file.name
                    with open(filename, "w", encoding="utf-8") as fh:
                        fh.write(obj)
            elif interaction.ui.serialization_format() == "source.yaml":
                with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False) as temp_file:
                    filename = temp_file.name
                    human_dump(obj=obj, filename=filename)
            elif interaction.ui.serialization_format() == "source.json":
                with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
                    filename = temp_file.name
                    with open(filename, "w", encoding="utf-8") as fh:
                        json.dump(obj, fh, indent=4, sort_keys=True)
            else:
                with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
                    filename = temp_file.name
                    with open(filename, "w", encoding="utf-8") as fh:
                        fh.write(obj)

        command = self._args.editor_command.format(filename=filename, line_number=line_number)
        is_console = self._args.editor_console

        self._logger.debug("Command: %s", command)
        if isinstance(command, str):
            if is_console:
                with SuspendCurses():
                    os.system(command)
            else:
                os.system(command)
        return None
