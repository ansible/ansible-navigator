"""stub action for replay
"""

from . import _actions as actions
from .run import Action as BaseAction


class MissingAttribute:
    # pylint: disable=too-few-public-methods
    """Raise an attribute error for any get"""

    def __get__(self, instance, owner):
        raise AttributeError()


@actions.register
class Action(MissingAttribute, BaseAction):

    # pylint: disable=too-many-instance-attributes
    """:replay"""

    KEGEX = r"""(?x)
            ^
            (?P<replay>rep(?:lay)?
            (\s(?P<params_replay>\S+))?)
            $"""

    run_stdout = MissingAttribute()  # type: ignore
