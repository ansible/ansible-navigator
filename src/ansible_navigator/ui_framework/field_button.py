"""A text input field."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .curses_window import Window
from .form_defs import FieldValidationStates
from .form_handler_button import FormHandlerButton
from .validators import FieldValidators


@dataclass
class FieldButton:
    """A text input field."""

    name: str
    text: str
    disabled: bool = True
    pressed: bool = False
    color: int = 0
    window_handler = FormHandlerButton
    validator: Callable = FieldValidators.none
    win: Window | None = None

    @property
    def full_prompt(self) -> str:
        """No default to add into the prompt for checkbox.

        :returns: Empty string
        """
        return ""

    def validate(self, response: FieldValidationStates) -> None:
        """Validate this instance.

        :param response: List of field states for validation.
        """
        validation = self.validator(response)
        if validation.error_msg:
            self.disabled = True
        else:
            self.disabled = False

    def conditional_validation(self, response: FieldValidationStates) -> None:
        """Conditional validation used for form validation.

        :param response: List of field states for validation.
        """
        self.validate(response)
