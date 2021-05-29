""" Get one line of text input
"""
import curses

from curses import ascii as curses_ascii
from typing import List
from typing import Tuple
from typing import TYPE_CHECKING

from .curses_defs import CursesLinePart
from .curses_window import CursesWindow


if TYPE_CHECKING:
    from .field_button import FieldButton  # pylint: disable=cyclic-import


class FormHandlerButton(CursesWindow):
    """handle form button"""

    def __init__(self, screen, ui_config):
        super().__init__(ui_config=ui_config)
        self._form_field = None
        self._form_fields = None
        self._screen = screen

    def populate(self):
        """populate the window with the button"""
        if self._form_field.disabled is True:
            color = 8
        else:
            color = self._form_field.color

        if self._ui_config.color is False:
            text = f"[{self._form_field.text.upper()}]"
        else:
            text = self._form_field.text

        clp_button = CursesLinePart(0, text, color, curses.A_STANDOUT)
        self._add_line(self.win, 0, ([clp_button]))

    def handle(self, idx, form_fields: List) -> Tuple["FieldButton", int]:
        """handle the check box field"""
        self._form_fields = form_fields
        self._form_field = form_fields[idx]
        self.populate()

        while True:
            char = self.win.getch()

            if char in [curses.KEY_RESIZE, curses_ascii.TAB]:
                break

            if char in [curses_ascii.NL, curses_ascii.CR]:
                if not self._form_field.disabled:
                    self._form_field.pressed = True
                break
        return self._form_field, char
