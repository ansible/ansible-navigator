""" individual check and the form field checks and radio
"""

from dataclasses import dataclass
from dataclasses import field
from functools import partial

from typing import Callable
from typing import List
from typing import Union

from .form_handler_options import FormHandlerOptions
from .sentinals import unknown
from .sentinals import Unknown
from .validators import FieldValidators
from .validators import Validation


@dataclass
class FieldRadio:

    # pylint: disable=too-many-instance-attributes
    """a form filed containing radios"""
    prompt: str
    name: str
    current_error: str = ""
    valid: Union[Unknown, bool] = unknown  # pylint: disable=unsubscriptable-object
    options: List = field(default_factory=list)
    window_handler = FormHandlerOptions

    @property
    def checked(self):
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
        return partial(FieldValidators.some_of_or_none, max_selected=1, min_selected=1)

    def _validate(self, response: "FieldRadio") -> Validation:
        validation = self.validator(choices=response.options)
        if validation.error_msg:
            self.valid = False
        else:
            self.valid = True
        return validation

    def validate(self, response: "FieldRadio") -> None:
        """validate this instance"""
        validation = self._validate(response)
        self.current_error = validation.error_msg

    def conditional_validation(self, response: "FieldRadio") -> None:
        """conditional validation used for
        tab
        """
        self._validate(response)
        self.current_error = ""
