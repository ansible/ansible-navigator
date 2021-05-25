""" common form defintions
"""

from enum import Enum


class FormType(Enum):
    """used indicate the form type"""

    FORM = "A full input form"
    NOTIFICATION = "A text box with a dismiss button"
    WORKING = "Used when something might take a bit, no buttons"
