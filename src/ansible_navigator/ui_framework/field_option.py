"""one option in either a check or radio field
"""
from dataclasses import dataclass
from typing import Union

from .field_checks import FieldChecks
from .field_radio import FieldRadio


@dataclass
class FieldOption:
    """one option in either a check or radio field"""

    name: str
    text: str
    checked: bool = False
    disabled: bool = False

    def ansi_code(self, form_field: Union[FieldChecks, FieldRadio]) -> str:
        """return our icon based on the
        form provided
        """
        if isinstance(form_field, FieldChecks):
            check_box = "\u25fc" if self.checked else "\u25fb"
            return check_box
        if isinstance(form_field, FieldRadio):
            check_box = "\u25cf" if self.checked else "\u25cb"
            return check_box
        raise TypeError
