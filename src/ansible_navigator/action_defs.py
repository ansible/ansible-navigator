"""Pre-defined objects used by actions."""

from __future__ import annotations

from typing import NamedTuple
from typing import Union


class RunReturn(NamedTuple):
    """The base return object for any action's run method."""

    #: A message to display immediately before exiting
    message: str
    #: The return code for the for the process
    return_code: int


class RunInteractiveReturn(RunReturn):
    """The return object for an action's run interactive method."""


class RunStdoutReturn(RunReturn):
    """The return object for an action's run stdout method."""


ActionReturn = Union[RunReturn, RunInteractiveReturn, RunStdoutReturn]
