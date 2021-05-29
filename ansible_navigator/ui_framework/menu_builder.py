""" build a menu
"""
import curses
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
        # pylint: disable=too-many-arguments
        self._number_colors = number_colors
        self._pbar_width = pbar_width
        self._screen_w = screen_w
        self._color_menu_item = color_menu_item
        self._ui_config = ui_config

    def build(self, dicts: List, cols: List, indicies) -> Tuple[CursesLines, CursesLines]:
        """main entry point for menu builer"""
        return self._menu(dicts, cols, indicies)

    def _menu(self, dicts: List, cols: List, indicies) -> Tuple[CursesLines, CursesLines]:
        """Build a text menu from a list of dicts given columns(root keys)

        :param dicts: A list of dicts
        :type dicts: list
        :param cols: The columns (keys) to use in the dicts
        :type cols: list of strings
        :return: the heading and body of the menu
        :param showing: A range of what's showing in the UI
        :type showing: Tuple(first, last)
        :rtype: (CursesLines, CursesLines)
        """
        line_prefix_w = len(str(len(dicts))) + len("|")

        for idx in indicies:
            convert_percentage(dicts[idx], cols, self._pbar_width)

        lines = [[str(dicts[idx].get(c)) for c in cols] for idx in indicies]
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
        menu_lines = self._menu_lines(dicts, menu_layout, indicies)
        return tuple([header]), menu_lines

    def _menu_header_line(self, menu_layout: Tuple[List, ...]) -> CursesLine:
        """Generate the menu header line

        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :return: the menu head line
        :type: CursesLine
        """
        _col_starts, cols, _adj_colws = menu_layout
        return tuple(self._menu_header_line_part(colno, menu_layout) for colno in range(len(cols)))

    @staticmethod
    def _menu_header_line_part(colno: int, menu_layout: Tuple[List, ...]) -> CursesLinePart:
        """Generate one part of the menu header line

        :param colno: The column number
        :type colno: int
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :return: the menu head line
        :type: CursesLinePart
        """
        col_starts, cols, adj_colws = menu_layout
        coltext = re.sub("^__", "", cols[colno])
        coltext = re.sub("_", " ", coltext)
        adj_entry = coltext[0 : adj_colws[colno]].upper()
        # right justifyheader if progress
        if cols[colno] == "__progress":
            return CursesLinePart(
                column=col_starts[colno] + adj_colws[colno] - len(adj_entry),
                string=adj_entry,
                color=0,
                decoration=curses.A_UNDERLINE,
            )
        return CursesLinePart(
            column=col_starts[colno], string=adj_entry, color=0, decoration=curses.A_UNDERLINE
        )

    def _menu_lines(
        self, dicts: List[Dict], menu_layout: Tuple[List, ...], indicies
    ) -> CursesLines:
        """Generate all the menu lines

        :params dicts: A list of dicts from which the menu will be generated
        :type dicts: List of Dicts
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :param menu_layout[3]: the menu header, used to determine justification
        :type memu_layout[3]: CursesLine
        :return: the menu lines
        :type: CursesLines
        """
        return tuple(self._menu_line(dicts[idx], menu_layout) for idx in indicies)

    def _menu_line(self, dyct: dict, menu_layout: Tuple[List, ...]) -> CursesLine:
        """Generate one the menu line

        :param dyct: One dict from which the menu line will be generated
        :type dyct: dict
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :param menu_layout[3]: the menu header, used to determine justification
        :type memu_layout[3]: CursesLine
        :return: a menu line
        :type: CursesLine
        """
        _col_starts, cols, _adj_colws, _header = menu_layout
        menu_line = (dyct.get(c) for c in cols)
        return tuple(
            self._menu_line_part(colno, coltext, dyct, menu_layout)
            for colno, coltext in enumerate(menu_line)
        )

    def _menu_line_part(
        self, colno: int, coltext: Any, dyct: dict, menu_layout: Tuple[List, ...]
    ) -> CursesLinePart:
        """Generate one menu line part

        :param colno: The column number of the line part
        :type colno: int
        :param coltext: The text to be placed at the given column
        :type: coltext: str
        :param dyct: the dict from which the menu line will be generated
        :type dyct: dict
        :param menu_layout: A tuple of menu details
        :type menu_layout: tuple
        :param menu_layout[0]: the starting in for each column
        :type menu_layout[0]: list of ints
        :param menu_layout[1]: the columns of the menu
        :type menu_layout[1]: list of strings
        :param menu_layout[2]: the adjusted column widths
        :type menu_layout[2]: list of ints
        :param menu_layout[3]: the menu header, used to determine justification
        :type memu_layout[3]: CursesLine
        :return: a menu line part
        :type: CursesLinePart
        """
        col_starts, cols, adj_colws, header = menu_layout

        color, decoration = self._color_menu_item(colno, cols[colno], dyct)

        text = str(coltext)[0 : adj_colws[colno]]
        if isinstance(coltext, (int, bool, float)) or cols[colno].lower() == "__duration":
            # right jusitfy on header if int, bool, float or "duration"
            print_at = col_starts[colno] + len(header[colno][1]) - len(text)
        elif cols[colno].lower() == "__progress":
            # right justify in column if progress indicator
            print_at = col_starts[colno] + adj_colws[colno] - len(text)
        else:
            # left justify
            print_at = col_starts[colno]
        return CursesLinePart(column=print_at, string=str(text), color=color, decoration=decoration)
