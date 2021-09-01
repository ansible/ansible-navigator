""" for def
"""
from dataclasses import dataclass, field
from typing import Dict
from typing import List

from .field_button import FieldButton
from .form_defs import FormType
from .form_presenter import FormPresenter
from .validators import FormValidators


@dataclass
class Form:
    """simple abstraction to hold the fields of the form
    and a convenience method to present it
    """

    type: FormType
    cancelled: bool = False
    fields: List = field(default_factory=list)
    submitted: bool = False
    title = ""
    title_color: int = 0

    _dict: Dict = field(default_factory=dict)

    def present(self, screen, ui_config):
        """present the form the to user and return the results"""
        if self.type is FormType.FORM:
            self.fields.append(
                FieldButton(
                    name="submit", text="Submit", validator=FormValidators.all_true, color=10
                )
            )
            self.fields.append(FieldButton(name="cancel", text="Cancel", color=9))
        elif self.type is FormType.NOTIFICATION:
            self.fields.append(
                FieldButton(
                    name="submit", text=" Ok ", validator=FormValidators.no_validation, color=10
                )
            )
        elif self.type is FormType.WORKING:
            pass

        FormPresenter(form=self, screen=screen, ui_config=ui_config).present()
        try:
            self.submitted = next(field for field in self.fields if field.name == "submit").pressed
        except StopIteration:
            self.submitted = False
        try:
            self.cancelled = next(field for field in self.fields if field.name == "cancel").pressed
        except StopIteration:
            self.cancelled = False
        return self
