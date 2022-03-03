"""a text input field
"""
from dataclasses import dataclass
from typing import Callable
from typing import Optional

from .curses_window import Window
from .form_defs import FieldValidationStates
from .form_handler_button import FormHandlerButton
from .validators import FieldValidators


@dataclass
class FieldButton:
    """a text input field"""

    name: str
    text: str
    disabled: bool = True
    pressed: bool = False
    color: int = 0
    window_handler = FormHandlerButton
    validator: Callable = FieldValidators.none
    win: Optional[Window] = None

    @property
    def full_prompt(self) -> str:
        """no default to add into the prompt for checkbox"""
        return ""

    def validate(self, response: FieldValidationStates) -> None:
        """validate this instance"""
        validation = self.validator(response)
        if validation.error_msg:
            self.disabled = True
        else:
            self.disabled = False

    def conditional_validation(self, response: FieldValidationStates) -> None:
        """conditional validation used for
        tab
        """
        self.validate(response)
