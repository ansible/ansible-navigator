"""information handler, instant enter
"""

from curses import ascii as curses_ascii
from typing import TYPE_CHECKING
from typing import List
from typing import Tuple

from .curses_window import CursesWindow


if TYPE_CHECKING:
    from .field_information import FieldInformation  # pylint: disable=cyclic-import


class FormHandlerInformation(CursesWindow):
    """handle form button"""

    def __init__(self, screen, ui_config):
        """Initialize the handler for a informational notification.

        :param screen: A curses window
        :param ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._screen = screen

    @staticmethod
    def handle(idx, form_fields: List) -> Tuple["FieldInformation", int]:
        """handle the information field, immediate return"""
        return form_fields[idx], curses_ascii.NL
