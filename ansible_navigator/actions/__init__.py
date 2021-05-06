""" actions for Explorer """
from typing import Callable
from typing import Union
from . import _actions as actions

from ..app_public import AppPublic
from ..configuration_subsystem import ApplicationConfiguration
from ..ui_framework import Interaction

get: Callable[[str], None] = actions.get_factory(__package__)

names = actions.names_factory(__package__)

kegexes: Callable = actions.kegexes_factory(__package__)

run_action_stdout: Callable[[str, ApplicationConfiguration], None] = actions.run_stdout_factory(
    __package__
)

run_action: Callable[
    [str, AppPublic, Interaction], Union[None, Interaction]
] = actions.run_interactive_factory(__package__)


__all__ = ["kegexes", "names", "run_action", "run_action_stdout"]
