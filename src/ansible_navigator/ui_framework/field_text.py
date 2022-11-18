"""A text input field."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from typing import Callable

from .curses_window import Window
from .form_handler_text import FormHandlerText
from .sentinels import Unknown
from .sentinels import nonexistent
from .sentinels import unknown
from .validators import FieldValidators


@dataclass
class FieldText:
    # pylint: disable=too-many-instance-attributes
    """A text input field."""

    name: str
    prompt: str
    current_error: str = ""
    default: Any = nonexistent
    window_handler = FormHandlerText
    response: str | Unknown = unknown
    valid: bool | Unknown = unknown
    validator: Callable = FieldValidators.none
    value: Any = unknown
    win: Window | None = None

    @property
    def formatted_default(self) -> str:
        """Return the default value.

        :returns: Default value or empty string
        """
        if self.default is nonexistent:
            return ""
        return f" ({self.default})"

    @property
    def full_prompt(self) -> str:
        """Return the full prompt with the default.

        :returns: Prompt with default text
        """
        return self.prompt + self.formatted_default

    def pre_populate(self, value: str) -> None:
        """Pre-populate this text input with a value.

        This is different from a default
        in that it will populate the text input field.

        :param value: Item to populate the input field
        """
        self.conditional_validation(str(value))

    def validate(self, response: str) -> None:
        """Validate the response.

        :param response: Text input response
        """
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
        """Conditional validation used for tab.

        Only accept the value if it validates, otherwise move along.

        :param response: Text input response
        """
        if response == "" and self.default is not nonexistent:
            response = str(self.default)
        # no response or validator is none
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
