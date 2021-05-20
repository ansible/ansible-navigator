""" a text imput field
"""
from dataclasses import dataclass

from typing import Callable
from typing import Union

from .curses_window import Window
from .form_handler_button import FormHandlerButton
from .validators import FieldValidators


@dataclass
class FieldButton:

    # pylint: disable=too-many-instance-attributes
    """a text inout field"""

    name: str
    text: str
    disabled: bool = True
    pressed: bool = False
    color: int = 0
    window_handler = FormHandlerButton
    validator: Callable = FieldValidators.none
    win: Union[Window, None] = None  # pylint: disable=unsubscriptable-object

    @property
    def full_prompt(self) -> str:
        """no default to add into the prompt for checkbox"""
        return ""

    def validate(self, response: "FieldButton") -> None:
        """validate this instance"""
        validation = self.validator(response)
        if validation.error_msg:
            self.disabled = True
        else:
            self.disabled = False

    def conditional_validation(self, response: "FieldButton") -> None:
        """conditional validation used for
        tab
        """
        self.validate(response)
