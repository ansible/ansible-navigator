"""Information handler, instant enter."""
from __future__ import annotations

from curses import ascii as curses_ascii
from typing import TYPE_CHECKING

from .curses_window import CursesWindow


if TYPE_CHECKING:
    from .field_information import FieldInformation


class FormHandlerInformation(CursesWindow):
    """Handle form button."""

    def __init__(self, screen, ui_config):
        """Initialize the handler for a informational notification.

        :param screen: A curses window
        :param ui_config: The current user interface configuration
        """
        super().__init__(ui_config=ui_config)
        self._screen = screen

    @staticmethod
    def handle(idx, form_fields: list) -> tuple[FieldInformation, int]:
        """Handle the information field, immediate return.

        :param idx: Index to retrieve specific field
        :param form_fields: List of fields
        :returns: Indexed form fields
        """
        return form_fields[idx], curses_ascii.NL
