"""Get one line of text input."""

from __future__ import annotations

import curses

from curses import ascii as curses_ascii
from curses.textpad import Textbox

from .curses_defs import CursesLine
from .curses_defs import CursesLinePart
from .curses_window import CursesWindow
from .sentinels import unknown


class FormHandlerText(CursesWindow, Textbox):
    """Get one line of text input."""

    def __init__(self, screen, ui_config):
        """Initialize the handler for a form text field.

        :param screen: A curses window
        :param ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self.input_line_cache = []
        self.input_line_pointer = 0
        self._arrowing = False
        self.insert_mode = False
        self.stripspaces = True
        self._screen = screen

    def _paint_from_line_cache(
        self,
    ) -> None:
        """Put the text from the line cache in the text input window."""
        line_part = CursesLinePart(0, self.input_line_cache[self.input_line_pointer], 0, 0)
        self._add_line(self.win, 0, CursesLine((line_part,)))
        self.win.clrtoeol()

    def _adjust_line_pointer(self, amount: int) -> None:
        """Increase the current position in the line cache.

        :param amount: The number to increase by
        """
        self.input_line_pointer = (self.input_line_pointer + amount) % len(self.input_line_cache)

    def _do_command(self, char: int) -> int:
        """Handle the input from the user.

        :param char: The character input from the user
        :returns: 0 if the window needs to be resized
                  1 if the window should be repainted
                  -1 if the window should be closed
        """
        # in the case the term returns 127 instead of 263
        if char == curses_ascii.DEL:
            char = curses.KEY_BACKSPACE

        if char == curses.KEY_IC:
            self.insert_mode = not self.insert_mode
            ret = 1
        elif char == curses_ascii.ESC:
            ret = -1
        elif char == curses.KEY_RESIZE:
            ret = 0
        elif char in (curses_ascii.SO, curses.KEY_DOWN):
            if self.input_line_cache:
                if not self._arrowing:
                    self.input_line_pointer = 0
                    self._arrowing = True
                else:
                    self._adjust_line_pointer(1)
                    self._paint_from_line_cache()
            ret = 1
        elif char in (curses_ascii.DLE, curses.KEY_UP):
            if self.input_line_cache:
                if not self._arrowing:
                    self.input_line_pointer = len(self.input_line_cache) - 1
                    self._arrowing = True
                else:
                    self._adjust_line_pointer(-1)
                    self._paint_from_line_cache()
            ret = 1
        elif char == curses_ascii.TAB:
            ret = 0
        else:
            ret = bool(self.do_command(char))  # type: ignore[func-returns-value]
            self._arrowing = 0
        return ret

    def handle(self, idx, form_fields) -> tuple[str, int]:
        """Edit in the widget window and collect the results.

        :param idx: Index to retrieve specific field
        :param form_fields: List of fields
        :returns: Results from line and char edit
        """
        form_field = form_fields[idx]

        if form_field.response is not unknown:
            line_part = CursesLinePart(0, form_field.response, 0, 0)
            self._add_line(self.win, 0, CursesLine((line_part,)))
        else:
            self.win.move(0, 0)

        self._curs_set(1)
        while True:
            char = self.win.getch()

            if not char:
                continue
            cmd_res = self._do_command(char)
            if cmd_res == 0:
                break
            if cmd_res == -1:
                return "", char
            self.win.refresh()
        self._curs_set(0)
        line = self.gather().strip()
        if line:
            self.input_line_cache.append(line)
        return line, char
