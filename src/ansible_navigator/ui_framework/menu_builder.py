"""Build a menu."""
from __future__ import annotations

import curses
import enum
import re

from typing import Any
from typing import Callable

from ansible_navigator.content_defs import ContentBase
from ansible_navigator.content_defs import ContentTypeSequence

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines
from .ui_config import UIConfig
from .utils import convert_percentage
from .utils import distribute


class MenuBuilder:
    """Build a menu from list of dicts."""

    def __init__(
        self,
        progress_bar_width: int,
        screen_width: int,
        number_colors: int,
        color_menu_item: Callable,
        ui_config: UIConfig,
    ):
        """Initialize the menu builder.

        :param progress_bar_width:  The width of the progress bar
        :param screen_width: The current screen width
        :param number_colors: The number of colors the current terminal supports
        :param color_menu_item: The callback for adding color to menu entries
        :param ui_config: The current user interface configuration
        """
        # pylint: disable=too-many-arguments
        self._number_colors = number_colors
        self._progress_bar_width = progress_bar_width
        self._screen_width = screen_width
        self._color_menu_item = color_menu_item
        self._ui_config = ui_config

    def build(
        self,
        dicts: ContentTypeSequence,
        cols: list[str],
        indices,
    ) -> tuple[CursesLines, CursesLines]:
        """Build menu main entry point.

        :param cols: he columns (keys) to use in the dicts
        :param dicts: A list of dicts
        :param indices: A range of what's showing in the UI
        :returns: The heading and body of a menu
        """
        return self._menu(dicts, cols, indices)

    def _menu(
        self,
        dicts: ContentTypeSequence,
        cols: list[str],
        indices,
    ) -> tuple[CursesLines, CursesLines]:
        """Build a text menu from a list of dicts given columns(root keys).

        :param dicts: A list of dicts
        :param cols: The columns (keys) to use in the dicts
        :param indices: A range of what's showing in the UI
        :returns: the heading and body of the menu
        """
        line_prefix_w = len(str(len(dicts))) + len("|")

        for idx in indices:
            convert_percentage(dicts[idx], cols, self._progress_bar_width)

        lines = [[str(dicts[idx].get(c)) for c in cols] for idx in indices]
        column_widths = [
            max(len(str(v)) for v in c)
            for c in zip(*lines + [[re.sub("^__", "", col) for col in cols]])
        ]
        # add a space
        column_widths = [c + 1 for c in column_widths]

        available = self._screen_width - line_prefix_w - 1  # scrollbar width
        adjusted_column_widths = distribute(available, column_widths)

        col_starts = [0]
        for idx, column_width in enumerate(adjusted_column_widths):
            col_starts.append(column_width + col_starts[idx])

        menu_layout = tuple([col_starts, cols, adjusted_column_widths])
        header = self._menu_header_line(menu_layout)

        menu_layout = tuple([col_starts, cols, adjusted_column_widths, header])
        menu_lines = self._menu_lines(dicts, menu_layout, indices)
        return CursesLines(tuple([header])), menu_lines

    def _menu_header_line(self, menu_layout: tuple[list, ...]) -> CursesLine:
        """Generate the menu header line.

        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
        :returns: The menu header line
        """
        _column_starts, cols, _adjusted_column_widths = menu_layout
        line_parts = tuple(
            self._menu_header_line_part(colno, menu_layout) for colno in range(len(cols))
        )
        return CursesLine(line_parts)

    @staticmethod
    def _menu_header_line_part(colno: int, menu_layout: tuple[list, ...]) -> CursesLinePart:
        """Generate one part of the menu header line.

        :param colno: The column number
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
        :returns: The menu head line
        """
        col_starts, cols, adjusted_column_widths = menu_layout
        coltext = re.sub("^__", "", cols[colno])
        coltext = re.sub("_", " ", coltext)
        adj_entry = coltext[0 : adjusted_column_widths[colno]].capitalize()
        # right justify header if progress
        if cols[colno] == "__progress":
            return CursesLinePart(
                column=col_starts[colno] + adjusted_column_widths[colno] - len(adj_entry),
                string=adj_entry,
                color=0,
                decoration=curses.A_UNDERLINE,
            )
        return CursesLinePart(
            column=col_starts[colno],
            string=adj_entry,
            color=0,
            decoration=curses.A_UNDERLINE,
        )

    def _menu_lines(
        self,
        dicts: ContentTypeSequence,
        menu_layout: tuple[list, ...],
        indices,
    ) -> CursesLines:
        """Generate all the menu lines.

        :param dicts: A list of dicts from which the menu will be generated
        :param indices: A range of what's showing in the UI
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
            * ``menu_layout[3]``: ``CursesLine``, the menu header, used to determine justification
        :returns: The menu lines
        """
        return CursesLines(tuple(self._menu_line(dicts[idx], menu_layout) for idx in indices))

    def _menu_line(
        self,
        menu_entry: dict[str, Any] | ContentBase,
        menu_layout: tuple[list, ...],
    ) -> CursesLine:
        """Generate one the menu line.

        :param menu_entry: One dict from which the menu line will be generated
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
            * ``menu_layout[3]``: ``CursesLine``, the menu header, used to determine justification
        :returns: A menu line
        """
        _column_starts, cols, _adjusted_column_widths, _header = menu_layout
        menu_line = (menu_entry.get(c) for c in cols)
        line_parts = (
            self._menu_line_part(colno, coltext, menu_entry, menu_layout)
            for colno, coltext in enumerate(menu_line)
        )
        return CursesLine(tuple(line_parts))

    def _menu_line_part(
        self,
        colno: int,
        coltext: Any,
        menu_entry: dict[str, Any] | ContentBase,
        menu_layout: tuple[list, ...],
    ) -> CursesLinePart:
        # pylint: disable=too-many-locals
        """Generate one menu line part.

        :param colno: The column number of the line part
        :param coltext: The text to be placed at the given column
        :param menu_entry: The dict from which the menu line will be generated
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
            * ``menu_layout[3]``: ``CursesLine``, the menu header, used to determine justification
        :returns: A menu line part
        """
        column_starts, cols, adjusted_column_widths, header = menu_layout

        color, decoration = self._color_menu_item(colno, cols[colno], menu_entry)

        text = str(coltext)[0 : adjusted_column_widths[colno]]

        is_bool = isinstance(coltext, bool)
        is_number = isinstance(coltext, (int, float))
        is_enum = isinstance(coltext, enum.Enum)
        is_duration = cols[colno].lower() == "__duration"
        is_progress = cols[colno].lower() == "__progress"

        if is_bool:
            # booleans are left justified
            print_at = column_starts[colno]
        elif is_number and not is_enum or is_duration:
            # right justify on header if int, float or "duration"
            print_at = column_starts[colno] + len(header[colno][1]) - len(text)
        elif is_progress:
            # right justify in column if progress indicator
            print_at = column_starts[colno] + adjusted_column_widths[colno] - len(text)
        else:
            # left justify
            print_at = column_starts[colno]
        return CursesLinePart(column=print_at, string=str(text), color=color, decoration=decoration)
