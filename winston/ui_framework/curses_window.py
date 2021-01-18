""" type for curses window
"""
import curses
import json
import logging
import os
from typing import TYPE_CHECKING
from typing import Union


# from .colorize import Colorize
from .colorize import hex_to_rgb_curses

# from .colorize import rgb_to_ansi

from .curses_defs import CursesLine

if TYPE_CHECKING:
    # pylint: disable= no-name-in-module
    from _curses import _CursesWindow

    Window = _CursesWindow
else:
    from typing import Any

    Window = Any


COLOR_MAP = {
    "terminal.ansiBlack": 0,
    "terminal.ansiRed": 1,
    "terminal.ansiGreen": 2,
    "terminal.ansiYellow": 3,
    "terminal.ansiBlue": 4,
    "terminal.ansiMagenta": 5,
    "terminal.ansiCyan": 6,
    "terminal.ansiWhite": 7,
    "terminal.ansiBrightBlack": 8,
    "terminal.ansiBrightRed": 9,
    "terminal.ansiBrightGreen": 10,
    "terminal.ansiBrightYellow": 11,
    "terminal.ansiBrightBlue": 12,
    "terminal.ansiBrightMagenta": 13,
    "terminal.ansiBrightCyan": 14,
    "terminal.ansiBrightWhite": 15,
}
DEFAULT_COLORS = "terminal_colors.json"


class CursesWindow:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """abstration for a curses window"""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        self._screen: Window
        self.win: Window
        self._screen_miny = 3
        self._prefix_color = 8
        self._no_osc4: bool
        self._theme_dir: str
        self._number_colors = 0
        self._custom_colors_enabled = False

    @property
    def _screen_w(self) -> int:
        """return the screen width

        :return: the current screen width
        :rtype: int
        """
        return self._screen.getmaxyx()[1]

    @property
    def _screen_h(self) -> int:
        """return the screen height, or notify if too small

        :return: the current screen height
        :rtype: int
        """
        while True:
            if self._screen.getmaxyx()[0] >= self._screen_miny:
                return self._screen.getmaxyx()[0] - 1
            curses.flash()
            curses.beep()
            self._screen.refresh()

    def _add_line(
        self, window: Window, lineno: int, line: CursesLine, prefix: Union[str, None] = None
    ) -> None:
        """add a line to a window

        :param window: A curses window
        :type window: Window
        :param lineno: the line number
        :type lineno: int
        :param line: The line to add
        :type line: CursesLine
        :param prefix: The prefix for the line
        :type prefix: str or None
        """
        win = window  # self.win if self.win else self._screen
        if prefix:
            win.addstr(
                lineno, 0, prefix, curses.color_pair(self._prefix_color % self._number_colors)
            )
        if line:
            win.move(lineno, 0)
            for line_part in line:
                column = line_part.column + len(prefix or "")
                if column <= self._screen_w:
                    text = line_part.string[0 : self._screen_w - column + 1]
                    try:
                        win.addstr(lineno, column, text, line_part.color | line_part.decoration)
                    except curses.error:
                        # curses error at last column but I don't care
                        # because it still draws it
                        # https://stackoverflow.com/questions/10877469/
                        # ncurses-setting-last-character-on-screen-without-scrolling-enabled
                        if lineno == self._screen_h and column + len(text) == self._screen_w:
                            pass
                        else:
                            self._logger.debug("curses error")
                            self._logger.debug("screen_h: %s, lineno: %s", self._screen_h, lineno)
                            self._logger.debug(
                                "screen_w: %s, column: %s text: %s, lentext: %s, end_col: %s",
                                self._screen_w,
                                column,
                                text,
                                len(text),
                                column + len(text),
                            )

    def _set_colors(self) -> None:
        """Set the colors for curses"""
        curses.use_default_colors()

        self._logger.debug("curses.COLORS: %s", curses.COLORS)
        self._logger.debug("curses.can_change_color: %s", curses.can_change_color())
        self._logger.debug("self._no_osc4: %s", self._no_osc4)
        if curses.COLORS > 16:
            if self._no_osc4 is True:
                self._custom_colors_enabled = False
            else:
                self._custom_colors_enabled = curses.can_change_color()
        else:
            self._custom_colors_enabled = False
        self._logger.debug("_custom_colors_enabled: %s", self._custom_colors_enabled)

        if self._custom_colors_enabled:
            with open(os.path.join(self._theme_dir, DEFAULT_COLORS)) as data_file:
                colors = json.load(data_file)

            for color_name, color_hex in colors.items():
                idx = COLOR_MAP[color_name]
                color = hex_to_rgb_curses(color_hex)
                curses.init_color(idx, *color)
            self._logger.debug("Custom colors set")
        else:
            self._logger.debug("Using terminal defaults")

        if self._custom_colors_enabled:
            # set to 16, since 17+ are used on demand for RGBs
            self._number_colors = 16
        else:
            # Stick to the define terminal colors, RGB will be mapped to these
            self._number_colors = curses.COLORS

        for i in range(0, self._number_colors):
            curses.init_pair(i, i, -1)
