""" actions for Explorer """
from typing import Callable
from typing import Union
from . import _actions as actions
from ..ui import Interaction


names = actions.names_factory(__package__)
run: Callable[[Interaction], Union[bool, Interaction]] = actions.call_factory(__package__)
kegexes: Callable = actions.kegexes_factory(__package__)
