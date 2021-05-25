""" an field with a 'working on it message'
"""
from dataclasses import dataclass

from typing import Callable
from typing import List
from typing import Union

from .curses_window import Window
from .form_handler_working import FormHandlerWorking
from .sentinals import unknown
from .sentinals import Unknown
from .validators import FieldValidators


@dataclass
class FieldWorking:

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=unsubscriptable-object
    """a text inout field"""
    name: str
    messages: List[str]
    current_error: str = ""
    window_handler = FormHandlerWorking
    valid: Union[bool, Unknown] = unknown
    validator: Callable = FieldValidators.null
    win: Union[Window, None] = None

    @property
    def full_prompt(self) -> str:
        """return the max width information since
        windows width and : placement is based on
        the largest 'prompt'
        """
        return max(self.messages)

    def validate(self, response: str) -> None:
        # pylint: disable=unused-argument
        """no validation required for working field"""
        self.valid = True

    def conditional_validation(self, response: str) -> None:
        # pylint: disable=unused-argument
        """no conditional validation"""
        self.validate(response)
