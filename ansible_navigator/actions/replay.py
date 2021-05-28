"""stub action for replay
"""

from . import _actions as actions
from .run import Action as BaseAction


@actions.register
class Action(BaseAction):

    # pylint: disable=too-many-instance-attributes
    """:replay"""

    @property
    def mode(self):
        return self._args.mode

    def run_stdout(self) -> int:
        """Replay artifact file with mode stdout"""
        return int(self._init_replay())

    KEGEX = r"""(?x)
            ^
            (?P<replay>rep(?:lay)?
            (\s(?P<params_replay>\S+))?)
            $"""
