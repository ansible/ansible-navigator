""" a text imput field
"""
from dataclasses import dataclass

from typing import Any
from typing import Callable
from typing import Union

from .curses_window import Window
from .form_handler_text import FormHandlerText
from .sentinals import nonexistent
from .sentinals import unknown
from .sentinals import Unknown
from .validators import FieldValidators


@dataclass
class FieldText:

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=unsubscriptable-object
    """a text inout field"""
    name: str
    prompt: str
    current_error: str = ""
    default: Any = nonexistent
    window_handler = FormHandlerText
    response: Union[str, Unknown] = unknown
    valid: Union[bool, Unknown] = unknown
    validator: Callable = FieldValidators.none
    value: Any = unknown
    win: Union[Window, None] = None

    @property
    def formatted_default(self) -> str:
        """return the default value"""
        if self.default is nonexistent:
            return ""
        return f" ({self.default})"

    @property
    def full_prompt(self) -> str:
        """the full rpompt includes the default"""
        return self.prompt + self.formatted_default

    def pre_populate(self, value: str) -> None:
        """prepopulate this text input
        with a value, this is different that a default
        in that it will populate the text input field
        """
        self.conditional_validation(str(value))

    def validate(self, response: str) -> None:
        """validate the repsonse"""
        if response == "" and self.default is not nonexistent:
            response = str(self.default)

        self.response = response
        validation = self.validator(text=response)
        self.current_error = validation.error_msg
        if validation.error_msg:
            self.valid = False
        else:
            self.valid = True
            self.value = validation.value

    def conditional_validation(self, response: str) -> None:
        """conditional validation used for tab,
        only accept the value if it validates, otherwise move along
        """
        if response == "" and self.default is not nonexistent:
            response = str(self.default)
        # no repsonse or validator is none
        if response or getattr(self.validator, "__name__", "").endswith("none"):
            validation = self.validator(text=response)
            if not validation.error_msg:
                self.validate(response)
                return
            self.response = response
        else:
            self.response = unknown
        self.valid = unknown
        self.current_error = ""
