""" Get one line of text input
"""
import curses
from curses.textpad import Textbox
from curses import ascii as curses_ascii
from typing import Callable


class OneLineInput(Textbox):
    """Get one line of text input"""

    def __init__(self):  # pylint: disable=super-init-not-called
        self.input_line_cache = []
        self.input_line_pointer = 0
        self._arrowing = False
        self.win = None
        self.maxx = None
        self.insert_mode = False

    def init_screen(self, *args, **kwargs):
        """init the super with a window and other args"""
        super().__init__(*args, **kwargs)

    def _paint_from_line_cache(self) -> None:
        """put the text from the line cache in the text input window"""
        if self.win:
            self.win.move(0, 0)
            text = self.input_line_cache[self.input_line_pointer]
            self.win.addnstr(text, self.maxx)
            self.win.clrtoeol()

    def _adjust_line_pointer(self, amount: int) -> None:
        """increase the curent postion in the
        line cache
        """
        self.input_line_pointer = (self.input_line_pointer + amount) % len(self.input_line_cache)

    def _do_command(self, char: int) -> int:
        if char == curses.KEY_IC:
            self.insert_mode = not self.insert_mode
            ret = 1
        elif char == curses_ascii.ESC:
            ret = -1
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
        else:
            ret = bool(self.do_command(char))  # type: ignore
            self._arrowing = 0
        return ret

    def edit(self, validate: Callable = None) -> str:
        "Edit in the widget window and collect the results."

        self.win.move(0, 0)
        self.win.clrtoeol()

        while True:
            char = self.win.getch()
            if validate:
                char = validate(char)
            if not char:
                continue
            cmd_res = self._do_command(char)
            if cmd_res == 0:
                break
            if cmd_res == -1:
                return ""
            self.win.refresh()
        line = self.gather().strip()
        if line:
            self.input_line_cache.append(line)
        return line
