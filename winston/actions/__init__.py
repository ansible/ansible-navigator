""" actions for Explorer """
from typing import Callable
from typing import Union
from . import _actions as actions
from ..ui import Interaction
from ..app_public import AppPublic

names = actions.names_factory(__package__)


run: Callable[[str, AppPublic, Interaction], Union[None, Interaction]] = actions.call_factory(
    __package__
)
kegexes: Callable = actions.kegexes_factory(__package__)


__all__ = ["kegexes", "names", "run"]
