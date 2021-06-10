""" Show a key overlay for presentations """

import time

import curses
from math import floor

try:
    from pyfiglet import Figlet
except ImportError:
    pass

from .curses_defs import CursesLinePart
from .curses_window import CursesWindow


class DemoMode(CursesWindow):
    # pylint: disable=too-few-public-methods
    """Functions specific to giving demos"""

    def __init__(self, screen, ui_config):
        super().__init__(ui_config=ui_config)
        self._figlet = Figlet(font="univers")
        self._screen = screen

    def show_key(self, string):
        """Show a single key on the screen"""

        if len(string) == 1 or string in ["^[", "KEY_NPAGE", "KEY_PPAGE"]:
            if string == "^[":
                string = "ESC"
            elif string == "KEY_NPAGE":
                string = "PgDn"
            elif string == "KEY_PPAGE":
                string = "PgUp"
            lines = self._figlet.renderText(string).splitlines()
            if len(lines) > self._screen_h:
                return
            top = floor((self._screen_h - len(lines)) / 2)
            max_line = max(len(line) for line in lines)
            if max_line > self._screen_w:
                return
            left = floor((self._screen_w - max_line) / 2)
            for idx, line in enumerate(lines):
                curses_line = (CursesLinePart(left, line, 0, curses.A_BOLD),)
                self._add_line(self._screen, top + idx, curses_line)
            self._screen.refresh()
            time.sleep(0.2)
