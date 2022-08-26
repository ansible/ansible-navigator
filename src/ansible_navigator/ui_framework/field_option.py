"""One option in either a check or radio field."""
from __future__ import annotations

from dataclasses import dataclass

from .field_checks import FieldChecks
from .field_radio import FieldRadio


@dataclass
class FieldOption:
    """One option in either a check or radio field."""

    name: str
    text: str
    checked: bool = False
    disabled: bool = False

    def ansi_code(self, form_field: FieldChecks | FieldRadio) -> str:
        """Return our icon based on the form provided.

        :param form_field: Form with check or radio field
        :raises TypeError: If form_field is not a check or radio field
        :returns: Check box icon
        """
        if isinstance(form_field, FieldChecks):
            check_box = "\u25fc" if self.checked else "\u25fb"
            return check_box
        if isinstance(form_field, FieldRadio):
            check_box = "\u25cf" if self.checked else "\u25cb"
            return check_box
        raise TypeError
