"""An information field formatted as curses lines."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .curses_defs import CursesLines
from .curses_window import Window
from .form_handler_information import FormHandlerInformation
from .sentinels import Unknown
from .sentinels import unknown
from .validators import FieldValidators


@dataclass
class FieldCursesInformation:
    """An information field made of curses lines."""

    name: str
    information: CursesLines
    current_error: str = ""
    window_handler = FormHandlerInformation
    valid: bool | Unknown = unknown
    validator: Callable = FieldValidators.null
    win: Window | None = None

    @property
    def full_prompt(self) -> str:
        """Return the max width string.

        :returns: The max width string
        """
        return max(
            (
                max((line_part for line_part in line), key=lambda lp: len(lp.string)).string
                for line in self.information
            ),
            key=len,
        )

    def validate(self, response: str) -> None:
        """No validation required for information field.

        :param response: The response to validate
        """
        self.valid = True

    def conditional_validation(self, response: str) -> None:
        """No conditional validation.

        :param response: The response to validate
        """
        self.validate(response)
