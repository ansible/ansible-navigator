"""``:open`` command implementation."""

from __future__ import annotations

import curses
import logging
import os

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

from ansible_navigator.content_defs import ContentBase
from ansible_navigator.content_defs import ContentFormat
from ansible_navigator.content_defs import ContentType
from ansible_navigator.content_defs import ContentView
from ansible_navigator.content_defs import SerializationFormat
from ansible_navigator.utils.functions import remove_dbl_un
from ansible_navigator.utils.serialize import serialize_write_temp_file

from . import _actions as actions


if TYPE_CHECKING:
    from collections.abc import Callable
    from re import Pattern
    from types import TracebackType

    from ansible_navigator.app_public import AppPublic
    from ansible_navigator.configuration_subsystem.definitions import ApplicationConfiguration
    from ansible_navigator.ui_framework import Interaction
    from ansible_navigator.ui_framework import Menu


class SuspendCurses:
    """Context Manager to temporarily leave curses mode."""

    def __enter__(self) -> None:
        """Close the curses window."""
        curses.endwin()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Open the curses window.

        Args:
            exc_type: The exception class
            exc_val: The type of exception
            traceback: Report of all information related to the
                exception
        """
        new_scr = curses.initscr()
        new_scr.refresh()
        curses.doupdate()


@actions.register
class Action:
    """``:open`` command implementation."""

    KEGEX = r"^o(?:pen)?(\s(?P<requested>.*))?$"

    def __init__(self, args: ApplicationConfiguration) -> None:
        """Initialize the ``:open`` action.

        Args:
            args: The current settings for the application
        """
        self._args = args
        self._logger = logging.getLogger(__name__)

    def _transform_menu(
        self,
        menu: Menu,
        menu_filter: Callable[..., Pattern[str] | None],
        serialization_format: SerializationFormat | None,
    ) -> list[dict[Any, Any] | ContentBase[Any]]:
        """Convert a menu into structured data.

        Args:
            menu: The current menu showing
            menu_filter: The effective menu filter
            serialization_format: The current serialization format

        Returns:
            The menu converted to a structured data
        """
        self._logger.debug("menu is showing, open that")
        menu_entries: list[dict[Any, Any] | ContentBase[Any]] = []
        for entry in menu.current:
            if isinstance(entry, ContentBase) and serialization_format is not None:
                entry = entry.asdict(
                    content_view=ContentView.FULL,
                    serialization_format=serialization_format,
                )
            menu_entries.append(entry)

        menu_entries = [
            {remove_dbl_un(k): v for k, v in c.items() if k in menu.columns} for c in menu_entries
        ]
        menu_filter_result = menu_filter()
        if menu_filter_result:
            menu_entries = [
                e
                for e in menu_entries
                if menu_filter_result.search(" ".join(str(v) for v in e.values()))  # type: ignore[union-attr]
            ]
        return menu_entries

    @staticmethod
    def _assess_requested_is_file(requested: str) -> tuple[Path | None, int | None]:
        """Determine is the user requested string is a file.

        Args:
            requested: The string requested at the ``:`` prompt

        Returns:
            None, None or file name and line number
        """
        parts = requested.rsplit(":", 1)
        possible_filename = Path(parts[0])
        if possible_filename.is_file():
            file_name = possible_filename
            try:
                line_number = int(parts[1:][0]) if parts[1:] else 0
            except ValueError:
                line_number = 0
            return file_name, line_number
        return None, None

    def _open_a_file(
        self,
        file_name: Path,
        line_number: int,
        editor_console: bool,
        editor_command: str,
    ) -> None:
        """Open a file using the editor.

        Args:
            file_name: The name of the file to open
            line_number: The line number the file should be opened at
            editor_console: Indicates if the editor is console based
            editor_command: The templatable editor command
        """
        command = editor_command.format(filename=file_name, line_number=line_number)

        self._logger.debug("Command: %s", command)
        if isinstance(command, str):
            if editor_console:
                with SuspendCurses():
                    os.system(command)  # noqa:S605
            else:
                os.system(command)  # noqa:S605

    @staticmethod
    def _persist_content(content: ContentType, content_format: ContentFormat) -> Path:
        """Write content to a temporary file.

        Args:
            content: the content to write
            content_format: The format of the content

        Returns:
            The path to the file
        """
        file_name = serialize_write_temp_file(
            content=content,
            content_view=ContentView.NORMAL,
            content_format=content_format,
        )
        return file_name

    def run(self, interaction: Interaction, app: AppPublic) -> None:
        """Execute the ``:open`` request for mode interactive.

        Args:
            interaction: The interaction from the user
            app: The app instance

        Returns:
            Nothing
        """
        self._logger.debug("open requested")

        editor_command = self._args.editor_command
        editor_console = self._args.editor_console
        requested = interaction.action.match.groupdict()["requested"]
        content_format = interaction.ui.content_format()
        serialization_format = content_format.value.serialization

        if requested:
            requested_file_name, requested_line_number = self._assess_requested_is_file(requested)
            if isinstance(requested_file_name, Path) and isinstance(requested_line_number, int):
                self._open_a_file(
                    file_name=requested_file_name,
                    line_number=requested_line_number,
                    editor_console=editor_console,
                    editor_command=editor_command,
                )
                return

            temp_file_name = self._persist_content(content=requested, content_format=content_format)
            temp_line_number = 0
            self._open_a_file(
                file_name=temp_file_name,
                line_number=temp_line_number,
                editor_console=editor_console,
                editor_command=editor_command,
            )
            return

        if interaction.content:
            content = interaction.content.showing
        elif interaction.menu:
            content = self._transform_menu(
                menu=interaction.menu,
                menu_filter=interaction.ui.menu_filter,
                serialization_format=serialization_format,
            )
        else:
            return

        content_file_name = self._persist_content(content=content, content_format=content_format)
        content_line_number = 0
        self._open_a_file(
            file_name=content_file_name,
            line_number=content_line_number,
            editor_console=editor_console,
            editor_command=editor_command,
        )
        return
