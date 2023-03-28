"""Individual field check, the form field checks and radio check."""
from __future__ import annotations

import sys

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
class FieldChecks:
    """A form field containing checks."""

    prompt: str
    name: str
    current_error: str = ""
    valid: Unknown | bool = unknown
    options: list = field(default_factory=list)
    max_selected: int = sys.maxsize
    min_selected: int = 1
    window_handler = FormHandlerOptions

    @property
    def checked(self) -> tuple[bool, ...]:
        """Conveniently return just checked fields.

        :returns: Name of every checked field
        """
        return tuple(option.name for option in self.options if option.checked)

    @property
    def formatted_default(self) -> str:
        """Format the checked field prompt with an empty string.

        :returns: Empty string
        """
        return ""

    @property
    def full_prompt(self) -> str:
        """Format the checkbox prompt.

        :returns: Checkbox prompt
        """
        return self.prompt

    @property
    def validator(self) -> Callable:
        """Provide a validator based on form type.

        :returns: Validation of checked entries
        """
        return partial(
            FieldValidators.some_of_or_none,
            max_selected=self.max_selected,
            min_selected=self.min_selected,
        )

    def _validate(self, response: FieldChecks) -> Validation:
        """Validate this FieldChecks instance.

        :param response: The form response from the user
        :returns: Validation of the response
        """
        validation = self.validator(choices=response.options)
        if validation.error_msg:
            self.valid = False
        else:
            self.valid = True
        return validation

    def validate(self, response: FieldChecks) -> None:
        """Validate this FieldChecks instance.

        :param response: Instance to check and verify options are valid
        """
        if self.max_selected == sys.maxsize:
            self.max_selected = len(self.options)

        validation = self._validate(response)
        self.current_error = validation.error_msg

    def conditional_validation(self, response: FieldChecks) -> None:
        """Conditional validation for a field_checks instance.

        :param response: Instance to check and verify options are valid
        """
        self._validate(response)
        self.current_error = ""
