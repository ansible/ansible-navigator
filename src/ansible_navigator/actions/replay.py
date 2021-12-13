"""stub action for replay
"""

from . import _actions as actions
from .run import Action as BaseAction


@actions.register
class Action(BaseAction):

    # pylint: disable=too-many-instance-attributes
    """:replay"""

    KEGEX = r"""(?x)
            ^
            (?P<replay>rep(?:lay)?
            (\s(?P<params_replay>\S+))?)
            $"""
