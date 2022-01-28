"""build a menu
"""
import curses
import enum
import re

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_defs import CursesLines
from .ui_config import UIConfig
from .utils import convert_percentage
from .utils import distribute


class MenuBuilder:
    # pylint: disable=too-few-public-methods
    """build a menu from list of dicts"""

    def __init__(
        self,
        pbar_width: int,
        screen_w: int,
        number_colors: int,
        color_menu_item: Callable,
        ui_config: UIConfig,
    ):
        """Initialize the menu builder.

        :param pbar_width:  The width of the progress bar
        :param screen_w: The current screen width
        :param number_colors: The number of colors the current terminal supports
        :param color_menu_item: The callback for adding color to menu entries
        :param ui_config: The current user interface configuration
        """
        # pylint: disable=too-many-arguments
        self._number_colors = number_colors
        self._pbar_width = pbar_width
        self._screen_w = screen_w
        self._color_menu_item = color_menu_item
        self._ui_config = ui_config

    def build(self, dicts: List, cols: List, indices) -> Tuple[CursesLines, CursesLines]:
        """main entry point for menu builder"""
        return self._menu(dicts, cols, indices)

    def _menu(self, dicts: List, cols: List[str], indices) -> Tuple[CursesLines, CursesLines]:
        """Build a text menu from a list of dicts given columns(root keys)

        :param dicts: A list of dicts
        :param cols: The columns (keys) to use in the dicts
        :param indices: A range of what's showing in the UI
        :return: the heading and body of the menu
        :rtype: (CursesLines, CursesLines)
        """
        line_prefix_w = len(str(len(dicts))) + len("|")

        for idx in indices:
            convert_percentage(dicts[idx], cols, self._pbar_width)

        lines = [[str(dicts[idx].get(c)) for c in cols] for idx in indices]
        colws = [
            max([len(str(v)) for v in c])
            for c in zip(*lines + [[re.sub("^__", "", col) for col in cols]])
        ]
        # add a space
        colws = [c + 1 for c in colws]

        available = self._screen_w - line_prefix_w - 1  # scrollbar width
        adj_colws = distribute(available, colws)

        col_starts = [0]
        for idx, colw in enumerate(adj_colws):
            col_starts.append(colw + col_starts[idx])

        menu_layout = tuple([col_starts, cols, adj_colws])
        header = self._menu_header_line(menu_layout)

        menu_layout = tuple([col_starts, cols, adj_colws, header])
        menu_lines = self._menu_lines(dicts, menu_layout, indices)
        return tuple([header]), menu_lines

    def _menu_header_line(self, menu_layout: Tuple[List, ...]) -> CursesLine:
        """Generate the menu header line

        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
        :return: The menu header line
        """
        _col_starts, cols, _adj_colws = menu_layout
        return tuple(self._menu_header_line_part(colno, menu_layout) for colno in range(len(cols)))

    @staticmethod
    def _menu_header_line_part(colno: int, menu_layout: Tuple[List, ...]) -> CursesLinePart:
        """Generate one part of the menu header line

        :param colno: The column number
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
        :return: The menu head line
        """
        col_starts, cols, adj_colws = menu_layout
        coltext = re.sub("^__", "", cols[colno])
        coltext = re.sub("_", " ", coltext)
        adj_entry = coltext[0 : adj_colws[colno]].upper()
        # right justify header if progress
        if cols[colno] == "__progress":
            return CursesLinePart(
                column=col_starts[colno] + adj_colws[colno] - len(adj_entry),
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

    def _menu_lines(self, dicts: List[Dict], menu_layout: Tuple[List, ...], indices) -> CursesLines:
        """Generate all the menu lines

        :params dicts: A list of dicts from which the menu will be generated
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
            * ``menu_layout[3]``: ``CursesLine``, the menu header, used to determine justification
        :return: The menu lines
        """
        return tuple(self._menu_line(dicts[idx], menu_layout) for idx in indices)

    def _menu_line(self, dyct: dict, menu_layout: Tuple[List, ...]) -> CursesLine:
        """Generate one the menu line

        :param dyct: One dict from which the menu line will be generated
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
            * ``menu_layout[3]``: ``CursesLine``, the menu header, used to determine justification
        :return: A menu line
        """
        _col_starts, cols, _adj_colws, _header = menu_layout
        menu_line = (dyct.get(c) for c in cols)
        return tuple(
            self._menu_line_part(colno, coltext, dyct, menu_layout)
            for colno, coltext in enumerate(menu_line)
        )

    def _menu_line_part(
        self,
        colno: int,
        coltext: Any,
        dyct: dict,
        menu_layout: Tuple[List, ...],
    ) -> CursesLinePart:
        """Generate one menu line part

        :param colno: The column number of the line part
        :param coltext: The text to be placed at the given column
        :param dyct: The dict from which the menu line will be generated
        :param menu_layout: A tuple of menu details:

            * ``menu_layout[0]``: ``List[int]``, the starting in for each column
            * ``menu_layout[1]``: ``List[str]``, the columns of the menu
            * ``menu_layout[2]``: ``List[int]``, the adjusted column widths
            * ``menu_layout[3]``: ``CursesLine``, the menu header, used to determine justification
        :return: A menu line part
        """
        col_starts, cols, adj_colws, header = menu_layout

        color, decoration = self._color_menu_item(colno, cols[colno], dyct)

        text = str(coltext)[0 : adj_colws[colno]]
        if (isinstance(coltext, (int, bool, float)) and not isinstance(coltext, enum.Enum)) or cols[
            colno
        ].lower() == "__duration":
            # right justify on header if int, bool, float or "duration"
            print_at = col_starts[colno] + len(header[colno][1]) - len(text)
        elif cols[colno].lower() == "__progress":
            # right justify in column if progress indicator
            print_at = col_starts[colno] + adj_colws[colno] - len(text)
        else:
            # left justify
            print_at = col_starts[colno]
        return CursesLinePart(column=print_at, string=str(text), color=color, decoration=decoration)
