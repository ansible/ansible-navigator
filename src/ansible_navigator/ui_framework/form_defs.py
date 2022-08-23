"""Common form definitions."""

from __future__ import annotations

from enum import Enum
from typing import List
from typing import Union

from .sentinels import Unknown


FieldValidationState = Union[Unknown, bool]
FieldValidationStates = List[FieldValidationState]


class FormType(Enum):
    """Indicates the form type."""

    FORM = "A full input form"
    NOTIFICATION = "A text box with a dismiss button"
    WORKING = "Used when something might take a bit, no buttons"
