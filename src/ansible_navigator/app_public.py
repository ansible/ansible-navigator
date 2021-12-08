"""A carrier for app internals.

This will be shared with other actions and is immutable.
"""
from typing import Callable
from typing import List
from typing import NamedTuple

from .configuration_subsystem import ApplicationConfiguration
from .steps import Steps


class AppPublic(NamedTuple):
    # pylint: disable=inherit-non-class
    # pylint: disable=too-few-public-methods
    """A carrier class for app internals.

    This will be shared with other actions and is immutable.
    """

    args: ApplicationConfiguration
    name: str
    rerun: Callable
    stdout: List[str]
    steps: Steps
    update: Callable
    write_artifact: Callable
