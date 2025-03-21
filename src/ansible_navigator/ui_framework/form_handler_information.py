"""Information handler, instant enter."""

from __future__ import annotations

from curses import ascii as curses_ascii
from typing import TYPE_CHECKING
from typing import Any

from .curses_window import CursesWindow
from .curses_window import Window


if TYPE_CHECKING:
    from ansible_navigator.ui_framework.ui_config import UIConfig

    from .field_information import FieldInformation


class FormHandlerInformation(CursesWindow):
    """Handle form button."""

    def __init__(self, screen: Window, ui_config: UIConfig) -> None:
        """Initialize the handler for a informational notification.

        Args:
            screen: A curses window
            ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._screen = screen

    @staticmethod
    def handle(idx: int, form_fields: list[Any]) -> tuple[FieldInformation, int]:
        """Handle the information field, immediate return.

        Args:
            idx: Index to retrieve specific field
            form_fields: List of fields

        Returns:
            Indexed form fields
        """
        return form_fields[idx], curses_ascii.NL
