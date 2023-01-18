"""Type for curses window."""
from __future__ import annotations

import curses
import json
import logging

from typing import TYPE_CHECKING

from .colorize import hex_to_rgb_curses
from .curses_defs import CursesLine
from .ui_config import UIConfig


if TYPE_CHECKING:
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


class CursesWindow:
    # pylint: disable=too-many-instance-attributes
    """Abstraction for a curses window."""

    def __init__(self, ui_config: UIConfig):
        """Initialize a curses window.

        :param ui_config: The current user interface configuration
        """
        self._logger = logging.getLogger(__name__)

        self._screen: Window
        self.win: Window
        self._screen_min_height = 3
        self._prefix_color = 8
        self._theme_dir: str
        self._term_osc4_support: bool
        self._ui_config = ui_config
        self._logger.debug("self._ui_config: %s", self._ui_config)
        self._set_colors()

    @property
    def _screen_width(self) -> int:
        """Return the screen width.

        :returns: the current screen width
        """
        return self._screen.getmaxyx()[1]

    @property
    def _screen_height(self) -> int:
        """Return the screen height, or notify if too small.

        :returns: the current screen height
        """
        while True:
            if self._screen.getmaxyx()[0] >= self._screen_min_height:
                return self._screen.getmaxyx()[0]
            curses.flash()
            curses.beep()
            self._screen.refresh()

    def _color_pair_or_none(self, color: int) -> int | None:
        """Return 0 if colors are disabled, otherwise returns the curses color pair.

        :param color: Int for specific curses color
        :returns: Curses color pair
        """
        if not self._ui_config.color or curses.COLORS == 0:
            return None
        color_arg = color % curses.COLORS  # self._number_colors
        return curses.color_pair(color_arg)

    def _curs_set(self, value: int):
        """Log an error in the case of a TERM with limited capabilities.

        :param value: TERM value
        """
        try:
            curses.curs_set(value)
        except curses.error:
            self._logger.error("Errors setting up terminal, check TERM value")

    def _add_line(
        self,
        window: Window,
        lineno: int,
        line: CursesLine,
        prefix: str | None = None,
    ) -> None:
        """Add a line to a window.

        :param window: A curses window
        :type window: Window
        :param lineno: the line number
        :type lineno: int
        :param line: The line to add
        :type line: CursesLine
        :param prefix: The prefix for the line
        :type prefix: str or None
        """
        if prefix:
            color = self._color_pair_or_none(self._prefix_color)
            if color is None:
                window.addstr(lineno, 0, prefix)
            else:
                window.addstr(lineno, 0, prefix, color)
        if line:
            window.move(lineno, 0)
            for line_part in line:
                column = line_part.column + len(prefix or "")
                if column <= self._screen_width:
                    text = line_part.string[0 : self._screen_width - column + 1]
                    try:
                        color = self._color_pair_or_none(line_part.color)
                        if color is None:
                            window.addstr(lineno, column, text)
                        else:
                            window.addstr(lineno, column, text, color | line_part.decoration)
                    except curses.error:
                        # curses error at last column & row but I don't care
                        # because it still draws it
                        # https://stackoverflow.com/questions/10877469/
                        # ncurses-setting-last-character-on-screen-without-scrolling-enabled
                        if (
                            lineno == window.getyx()[0]
                            and column + len(text) == window.getyx()[1] + 1
                        ):
                            pass

                        else:
                            self._logger.debug("curses error")
                            self._logger.debug(
                                "screen_height: %s, lineno: %s",
                                self._screen_height,
                                lineno,
                            )
                            self._logger.debug(
                                "screen_w: %s, column: %s text: %s, lentext: %s, end_col: %s",
                                self._screen_width,
                                column,
                                text,
                                len(text),
                                column + len(text),
                            )

    def _set_colors(self) -> None:
        """Set the colors for curses."""
        # curses colors may have already been initialized
        # with another instance of curses window
        if self._ui_config.colors_initialized is True:
            return

        self._curs_set(0)
        # in the case of a TERM with limited capabilities
        # disable color and get out fast
        try:
            curses.use_default_colors()
        except curses.error:
            self._logger.error("Errors setting up terminal, no color support")
            self._term_osc4_support = False
            self._ui_config.colors_initialized = True
            return

        self._logger.debug("curses.COLORS: %s", curses.COLORS)
        self._logger.debug("curses.can_change_color: %s", curses.can_change_color())

        self._term_osc4_support = curses.can_change_color()
        if self._ui_config.osc4 is False:
            self._term_osc4_support = False
        self._logger.debug("term_osc4_support: %s", self._term_osc4_support)

        if self._term_osc4_support:
            with self._ui_config.terminal_colors_path.open(mode="r", encoding="utf-8") as fh:
                colors = json.load(fh)

            for color_name, color_hex in colors.items():
                idx = COLOR_MAP[color_name]
                color = hex_to_rgb_curses(color_hex)
                curses.init_color(idx, *color)
            self._logger.debug("Custom colors set")
        else:
            self._logger.debug("Using terminal defaults")

        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)
        self._ui_config.colors_initialized = True
