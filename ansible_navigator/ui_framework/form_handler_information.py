""" information handler, instant enter
"""

from curses import ascii as curses_ascii
from typing import List
from typing import Tuple
from typing import TYPE_CHECKING

from .curses_window import CursesWindow


if TYPE_CHECKING:
    from .field_information import FieldInformation  # pylint: disable=cyclic-import


class FormHandlerInformation(CursesWindow):
    # pylint: disable=too-few-public-methods
    """handle form button"""

    def __init__(self, screen, ui_config):
        super().__init__(ui_config=ui_config)
        self._screen = screen

    @staticmethod
    def handle(idx, form_fields: List) -> Tuple["FieldInformation", int]:
        """handle the information field, immediate return"""
        return form_fields[idx], curses_ascii.NL
