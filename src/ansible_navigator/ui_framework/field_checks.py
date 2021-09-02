""" individual check and the form field checks and radio
"""
import sys

from dataclasses import dataclass
from dataclasses import field
from functools import partial

from typing import Callable
from typing import List
from typing import Tuple
from typing import Union


from .form_handler_options import FormHandlerOptions
from .sentinals import unknown
from .sentinals import Unknown
from .validators import FieldValidators
from .validators import Validation


@dataclass
class FieldChecks:

    # pylint: disable=too-many-instance-attributes
    """a form filed containing checks"""
    prompt: str
    name: str
    current_error: str = ""
    valid: Union[Unknown, bool] = unknown  # pylint: disable=unsubscriptable-object
    options: List = field(default_factory=list)
    max_selected: int = sys.maxsize
    min_selected: int = 1
    window_handler = FormHandlerOptions

    @property
    def checked(self) -> Tuple[bool, ...]:
        """conveniently return just checked"""
        return tuple(option.name for option in self.options if option.checked)

    @property
    def formatted_default(self) -> str:
        """check don't have a default to show in the
        prompt
        """
        return ""

    @property
    def full_prompt(self) -> str:
        """no default to add into the prompt for checkbox"""
        return self.prompt

    @property
    def validator(self) -> Callable:
        """based on form type, provide a validator"""
        return partial(
            FieldValidators.some_of_or_none,
            max_selected=self.max_selected,
            min_selected=self.min_selected,
        )

    def _validate(self, response: "FieldChecks") -> Validation:
        validation = self.validator(choices=response.options)
        if validation.error_msg:
            self.valid = False
        else:
            self.valid = True
        return validation

    def validate(self, response: "FieldChecks") -> None:
        """validate this instance"""
        if self.max_selected == sys.maxsize:
            self.max_selected = len(self.options)

        validation = self._validate(response)
        self.current_error = validation.error_msg

    def conditional_validation(self, response: "FieldChecks") -> None:
        """conditional validation used for
        tab
        """
        self._validate(response)
        self.current_error = ""
