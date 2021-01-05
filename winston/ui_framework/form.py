""" for def
"""
from dataclasses import dataclass, field
from typing import Dict
from typing import List

from .field_button import FieldButton
from .field_validators import FieldValidators
from .form_presenter import FromPresenter


@dataclass
class Form:
    """simple abstraction to hold the fields of the form
    and a convenience method to present it
    """

    fields: List = field(default_factory=list)
    submitted: bool = False
    cancelled: bool = False
    title = ""
    _dict: Dict = field(default_factory=dict)

    def present(self, stdscrn):
        """present the form the to user and return the results"""
        self.fields.append(
            FieldButton(name="submit", text="Submit", validator=FieldValidators.all_true, color=10)
        )
        self.fields.append(FieldButton(name="cancel", text="Cancel", color=9))
        FromPresenter(form=self).present(stdscrn)
        self.submitted = self.fields[-2].pressed
        self.cancelled = self.fields[-1].pressed
        return self
