"""Replay subcommand implementation.

A stub, the logic is used from ``:run``, only here as a place
to put the kegex.
"""


from . import _actions as actions
from .run import Action as BaseAction


@actions.register
class Action(BaseAction):
    """``:replay`` command implementation."""

    KEGEX = r"""(?x)
            ^
            (?P<replay>rep(?:lay)?
            (\s(?P<params_replay>\S+))?)
            $"""
