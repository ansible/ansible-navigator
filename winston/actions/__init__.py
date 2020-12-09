""" actions for Explorer """
from . import _actions as actions

names = actions.names_factory(__package__)
run = actions.call_factory(__package__)
kegexes = actions.kegexes_factory(__package__)
