"""stub action for load
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
    """:load"""

    KEGEX = r"""(?x)
            ^
            (?P<load>l(?:oad)?
            (\s(?P<params_load>\S+))?)
            $"""

    run_stdout = MissingAttribute()  # type: ignore
