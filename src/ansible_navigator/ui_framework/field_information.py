"""An information field."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .curses_window import Window
from .form_handler_information import FormHandlerInformation
from .sentinels import Unknown
from .sentinels import unknown
from .validators import FieldValidators


@dataclass
class FieldInformation:
    """A text input field."""

    name: str
    information: list[str]
    current_error: str = ""
    window_handler = FormHandlerInformation
    valid: bool | Unknown = unknown
    validator: Callable = FieldValidators.null
    win: Window | None = None

    @property
    def full_prompt(self) -> str:
        """Return the max width information.

        Windows width and : placement is based on
        the largest 'prompt'.

        :returns: Max width information
        """
        return max(self.information)

    def validate(self, response: str) -> None:
        """No validation required for information field.

        :param response: Field data
        """
        self.valid = True

    def conditional_validation(self, response: str) -> None:
        """No conditional validation required.

        :param response: Field data
        """
        self.validate(response)
