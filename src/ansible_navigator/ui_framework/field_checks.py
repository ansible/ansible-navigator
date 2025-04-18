"""Individual field check, the form field checks and radio check."""

from __future__ import annotations

import sys

from dataclasses import dataclass
from dataclasses import field
from functools import partial
from typing import TYPE_CHECKING
from typing import Any

from .form_handler_options import FormHandlerOptions
from .sentinels import Unknown
from .sentinels import unknown
from .validators import FieldValidators
from .validators import Validation


if TYPE_CHECKING:
    from collections.abc import Callable

    from ansible_navigator.ui_framework.curses_window import Window


@dataclass
class FieldChecks:
    # pylint: disable=too-many-instance-attributes
    """A form field containing checks."""

    prompt: str
    name: str
    current_error: str = ""
    valid: Unknown | bool = unknown
    options: list[Any] = field(default_factory=list)
    max_selected: int = sys.maxsize
    min_selected: int = 1
    window_handler = FormHandlerOptions
    win: Window | None = None

    @property
    def checked(self) -> tuple[bool, ...]:
        """Conveniently return just checked fields.

        Returns:
            Name of every checked field
        """
        return tuple(option.name for option in self.options if option.checked)

    @property
    def formatted_default(self) -> str:
        """Format the checked field prompt with an empty string.

        Returns:
            Empty string
        """
        return ""

    @property
    def full_prompt(self) -> str:
        """Format the checkbox prompt.

        Returns:
            Checkbox prompt
        """
        return self.prompt

    @property
    def validator(self) -> Callable[..., Any]:
        """Provide a validator based on form type.

        Returns:
            Validation of checked entries
        """
        return partial(
            FieldValidators.some_of_or_none,
            max_selected=self.max_selected,
            min_selected=self.min_selected,
        )

    def _validate(self, response: FieldChecks) -> Validation:
        """Validate this FieldChecks instance.

        Args:
            response: The form response from the user

        Returns:
            Validation of the response
        """
        validation = self.validator(choices=response.options)
        if validation.error_msg:
            self.valid = False
        else:
            self.valid = True
        return validation

    def validate(self, response: FieldChecks) -> None:
        """Validate this FieldChecks instance.

        Args:
            response: Instance to check and verify options are valid
        """
        if self.max_selected == sys.maxsize:
            self.max_selected = len(self.options)

        validation = self._validate(response)
        self.current_error = validation.error_msg

    def conditional_validation(self, response: FieldChecks) -> None:
        """Conditional validation for a field_checks instance.

        Args:
            response: Instance to check and verify options are valid
        """
        self._validate(response)
        self.current_error = ""
