"""working handler, instant 1112065
utf-8 max = 112064
"""

from typing import TYPE_CHECKING
from typing import List
from typing import Tuple

from .curses_window import CursesWindow


if TYPE_CHECKING:
    from .field_working import FieldWorking  # pylint: disable=cyclic-import


class FormHandlerWorking(CursesWindow):
    """handle form button"""

    def __init__(self, screen, ui_config):
        """Initialize the handler for a form working notification.

        :param screen: A curses window
        :param ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._screen = screen

    @staticmethod
    def handle(idx, form_fields: List) -> Tuple["FieldWorking", int]:
        """handle the information field, immediate return"""
        return form_fields[idx], 112065
