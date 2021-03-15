""" one option in either a check or radio field
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

    # pylint: disable=unsubscriptable-object
    def ansi_code(self, form_field: Union[FieldChecks, FieldRadio]) -> str:
        """return our icon based on the
        form provided
        """
        if isinstance(form_field, FieldChecks):
            cbox = "\u25fc" if self.checked else "\u25fb"
            return cbox
        if isinstance(form_field, FieldRadio):
            cbox = "\u25cf" if self.checked else "\u25cb"
            return cbox
        raise TypeError
