""" :open """
import curses
import json
import logging
import os
import tempfile

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Match
from typing import Tuple
from typing import Union

from . import _actions as actions
from ..app_public import AppPublic

from ..ui_framework import Content
from ..ui_framework import Interaction
from ..ui_framework import Menu

from ..utils import templar
from ..yaml import human_dump


class SuspendCurses:
    """Context Manager to temporarily leave curses mode"""

    def __enter__(self):
        curses.endwin()

    def __exit__(self, exc_type, exc_val, tback):
        newscr = curses.initscr()
        newscr.refresh()
        curses.doupdate()


@actions.register
class Action:
    """:open"""

    # pylint: disable=too-few-public-methods

    KEGEX = r"^o(?:pen)?(\s(?P<something>.*))?$"

    def __init__(self, args):
        self._args = args
        self._logger = logging.getLogger(__name__)

    def _content(self, content: Content, match: Match) -> Tuple[Union[str, None], str, Any]:
        filename = None
        line_number = "0"
        obj = None
        self._logger.debug("content is showing")
        something = match.groupdict()["something"]
        if something:
            self._logger.debug("asked to open something")
            if something.startswith("{{"):
                self._logger.debug("something appears to be a template: %s", something)
                templated = templar(something, content.showing)
                if isinstance(templated, str):
                    parts = templated.rsplit(":", 1)
                    if os.path.isfile(parts[0]):
                        filename = parts[0]
                        line_number = parts[1:][0] if parts[1:] else line_number
                        self._logger.debug(
                            "template interaction in valid filename %s:%s", filename, line_number
                        )
                    else:
                        self._logger.debug("template not a valid filename, open showing")
                        obj = templated
                else:
                    self._logger.debug("template not a string, open showing")
                    obj = templated
            else:
                parts = something.rsplit(":", 1)
                if os.path.isfile(parts[0]):
                    filename = parts[0]
                    line_number = parts[1:][0] if parts[1:] else line_number
                    self._logger.debug(
                        "something not a template, but is a valid filename %s:%s",
                        filename,
                        line_number,
                    )
                else:
                    self._logger.debug("something just a plain string")
                    obj = something
        else:
            self._logger.debug("something not provided")
            obj = content.showing
        return filename, line_number, obj

    @staticmethod
    def _remove_dbl_un(string):
        if string.startswith("__"):
            return string.replace("__", "", 1)
        return string

    def _menu(self, menu: Menu, menu_filter: Callable) -> Tuple[None, str, List[Dict[Any, Any]]]:
        filename = None
        line_number = "0"
        self._logger.debug("menu is showing, open that")
        obj = [
            {self._remove_dbl_un(k): v for k, v in c.items() if k in menu.columns}
            for c in menu.current
        ]
        if menu_filter():
            obj = [e for e in obj if menu_filter().search(" ".join(str(v) for v in e.values()))]
        return filename, line_number, obj

    # pylint: disable=too-many-branches
    def run(self, interaction: Interaction, app: AppPublic) -> None:
        # pylint: disable=too-many-branches
        # pylint: disable=unused-argument
        """Handle :open

        :param interaction: The interaction from the user
        :type interaction: Interaction
        :param app: The app instance
        :type app: App
        """
        self._logger.debug("open requested")
        if interaction.content:
            filename, line_number, obj = self._content(
                content=interaction.content, match=interaction.action.match
            )
        elif interaction.menu:
            filename, line_number, obj = self._menu(
                menu=interaction.menu, menu_filter=interaction.ui.menu_filter
            )
        else:
            return None

        if not filename:
            if interaction.ui.xform() == "text.html.markdown":
                filename = tempfile.NamedTemporaryFile(suffix=".md").name
                with open(filename, "w") as outfile:
                    outfile.write(obj)
            elif interaction.ui.xform() == "source.yaml":
                filename = tempfile.NamedTemporaryFile(suffix=".yaml").name
                human_dump(obj=obj, filename=filename)
            elif interaction.ui.xform() == "source.json":
                filename = tempfile.NamedTemporaryFile(suffix=".json").name
                with open(filename, "w") as outfile:
                    json.dump(obj, outfile, indent=4, sort_keys=True)
            else:
                filename = tempfile.NamedTemporaryFile(suffix=".txt").name
                with open(filename, "w") as outfile:
                    outfile.write(obj)

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
