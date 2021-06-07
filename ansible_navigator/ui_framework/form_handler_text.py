""" Get one line of text input
"""

import curses
from curses.textpad import Textbox
from curses import ascii as curses_ascii
from typing import Tuple


from .curses_defs import CursesLinePart
from .curses_window import CursesWindow
from .sentinals import unknown


class FormHandlerText(CursesWindow, Textbox):
    """Get one line of text input"""

    def __init__(self, screen, ui_config):
        super().__init__(ui_config=ui_config)
        self.input_line_cache = []
        self.input_line_pointer = 0
        self._arrowing = False
        self.insert_mode = False
        self.stripspaces = True
        self._screen = screen

    def _paint_from_line_cache(self) -> None:
        """put the text from the line cache in the text input window"""
        clp = CursesLinePart(0, self.input_line_cache[self.input_line_pointer], 0, 0)
        cline = (clp,)
        self._add_line(self.win, 0, cline)
        self.win.clrtoeol()

    def _adjust_line_pointer(self, amount: int) -> None:
        """increase the curent postion in the
        line cache
        """
        self.input_line_pointer = (self.input_line_pointer + amount) % len(self.input_line_cache)

    def _do_command(self, char: int) -> int:
        # pylint: disable=too-many-branches

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
            ret = bool(self.do_command(char))  # type: ignore
            self._arrowing = 0
        return ret

    def handle(self, idx, form_fields) -> Tuple[str, int]:
        "Edit in the widget window and collect the results."
        form_field = form_fields[idx]

        if form_field.response is not unknown:
            clp = CursesLinePart(0, form_field.response, 0, 0)
            self._add_line(self.win, 0, tuple([clp]))
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
