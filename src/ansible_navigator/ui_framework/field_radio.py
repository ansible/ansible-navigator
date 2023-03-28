"""Individual check and the form field checks for radios."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from functools import partial
from typing import Callable

from .form_handler_options import FormHandlerOptions
from .sentinels import Unknown
from .sentinels import unknown
from .validators import FieldValidators
from .validators import Validation


@dataclass
class FieldRadio:
    """A form field containing radios."""

    prompt: str
    name: str
    current_error: str = ""
    valid: Unknown | bool = unknown
    options: list = field(default_factory=list)
    window_handler = FormHandlerOptions

    @property
    def checked(self):
        """Conveniently return just checked options.

        :returns: Checked options
        """
        return tuple(option.name for option in self.options if option.checked)

    @property
    def formatted_default(self) -> str:
        """Format the field prompt with an empty string.

        :returns: Empty string
        """
        return ""

    @property
    def full_prompt(self) -> str:
        """Format the prompt.

        :returns: Prompt
        """
        return self.prompt

    @property
    def validator(self) -> Callable:
        """Provide a validator based on form type.

        :returns: Validation of checked entries
        """
        return partial(FieldValidators.some_of_or_none, max_selected=1, min_selected=1)

    def _validate(self, response: FieldRadio) -> Validation:
        """Validate this FieldRadio instance.

        :param response: The form response from the user
        :returns: Validation of the response
        """
        validation = self.validator(choices=response.options)
        if validation.error_msg:
            self.valid = False
        else:
            self.valid = True
        return validation

    def validate(self, response: FieldRadio) -> None:
        """Validate this FieldRadio instance.

        :param response: Instance to check and verify options are valid
        """
        validation = self._validate(response)
        self.current_error = validation.error_msg

    def conditional_validation(self, response: FieldRadio) -> None:
        """Conditional validation for a FieldRadio instance.

        :param response: Instance to check and verify options are valid
        """
        self._validate(response)
        self.current_error = ""
