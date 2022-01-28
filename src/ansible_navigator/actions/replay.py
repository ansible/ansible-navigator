"""stub action for replay
"""

from . import _actions as actions
from .run import Action as BaseAction


@actions.register
class Action(BaseAction):
    """:replay"""

    KEGEX = r"""(?x)
            ^
            (?P<replay>rep(?:lay)?
            (\s(?P<params_replay>\S+))?)
            $"""
