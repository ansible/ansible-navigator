""" Show a key overlay for presentations """
import re
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
                string = "Esc"
            elif string == "KEY_NPAGE":
                string = "PgDn"
            elif string == "KEY_PPAGE":
                string = "PgUp"
            lines = self._figlet.renderText(string).splitlines()
            # find the least number of right spaces in all lines
            right_trim = min(
                len(getattr(re.search(r"\s+$", line), "group", lambda: "")()) for line in lines
            )
            # find the least number of left spaces in all lines
            left_trim = min(
                len(getattr(re.search(r"^\s+", line), "group", lambda: "")()) for line in lines
            )
            # trim all lines
            lines = [f" {line[left_trim:-right_trim]} " for line in lines]

            # find first and last lines that aren't all blanks
            first_line = [idx for idx, line in enumerate(lines) if line.strip()][0]
            last_line = (
                len(lines) - [idx for idx, line in enumerate(reversed(lines)) if line.strip()][0]
            )
            lines = lines[first_line:last_line]

            # pad the lines at top and bottom
            max_line = max(len(line) for line in lines)
            lines.insert(0, " " * max_line)
            lines.append(" " * max_line)

            # bail if screen not tall/wide enough
            if len(lines) > self._screen_h:
                return
            if max_line > self._screen_w:
                return

            # center the overlay
            top = floor((self._screen_h - len(lines)) / 2)
            left = floor((self._screen_w - max_line) / 2)
            for idx, line in enumerate(lines):
                curses_line = (CursesLinePart(left, line, 0, curses.A_BOLD),)
                self._add_line(self._screen, top + idx, curses_line)
            self._screen.refresh()
            time.sleep(0.2)
