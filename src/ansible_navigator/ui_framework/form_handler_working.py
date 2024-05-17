"""Working handler, instant 1112065, utf-8 max = 112064."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .curses_window import CursesWindow
from .curses_window import Window


if TYPE_CHECKING:
    from ansible_navigator.ui_framework.ui_config import UIConfig

    from .field_working import FieldWorking


class FormHandlerWorking(CursesWindow):
    """Handle form button."""

    def __init__(self, screen: Window, ui_config: UIConfig) -> None:
        """Initialize the handler for a form working notification.

        :param screen: A curses window
        :param ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._screen = screen

    @staticmethod
    def handle(idx: int, form_fields: list[FieldWorking]) -> tuple[FieldWorking, int]:
        """Handle the information field, immediate return.

        :param idx: Index to retrieve specific field
        :param form_fields: List of fields from a form
        :returns: Indexed form fields
        """
        return form_fields[idx], 112065
