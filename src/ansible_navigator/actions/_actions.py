"""Some action stuff"""


import functools
import importlib
import logging
import re
import sys

from collections import namedtuple
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple


# mypy/pylint idiom for py36 compatibility
# https://github.com/python/typeshed/issues/3500#issuecomment-560958608
if sys.version_info >= (3, 7):
    from importlib import resources
else:
    import importlib_resources as resources


logger = logging.getLogger(__name__)

# Basic structure for storing information about one action
ActionT = namedtuple("ActionT", ("name", "cls", "kegex"))

Kegex = namedtuple("Kegex", ("name", "kegex"))

# Dictionary with information about all registered actions
_ACTIONS: Dict[str, Dict] = {}


def _import(package: str, action: str) -> None:
    """Import the given action file from a package"""
    importlib.import_module(f"{package}.{action}")


def _import_all(package: str) -> None:
    """Import all actions in a package"""
    # The following ignore can be removed when python 3.6 support is not required.
    files = resources.contents(package)  # type: ignore[attr-defined]
    actions = [
        f[:-3] for f in files if f.endswith(".py") and f[0] != "_" and not f.startswith(".#")
    ]
    for action in actions:
        _import(package, action)


def register(cls: Any) -> Any:
    """Decorator for registering a new action"""
    package, _, action = cls.__module__.rpartition(".")
    pkg_info = _ACTIONS.setdefault(package, {})
    pkg_info[action] = ActionT(name=action, cls=cls, kegex=re.compile(cls.KEGEX))
    return cls


def get(package: str, action: str) -> Callable:
    """Get a given action"""
    _import(package, action)
    return _ACTIONS[package][action].cls


def get_factory(package: str) -> Callable:
    """Create a get() function for one package"""
    return functools.partial(get, package)


def kegex(package: str, action: str) -> Tuple:
    """Return a tuple of name, kegex for a action"""
    _import(package, action)
    return _ACTIONS[package][action]


def kegexes(package: str) -> Generator:
    """Return a tuple of tuples, name, kegex"""
    _import_all(package)
    return (kegex(package, name) for name in names(package))


def kegexes_factory(package: str) -> Callable:
    """Create a kegexs() function for all packages"""
    return functools.partial(kegexes, package)


def names(package: str) -> List:
    """List all actions in one package"""
    _import_all(package)
    return sorted(_ACTIONS[package])


def names_factory(package: str) -> Callable:
    """Create a names() function for one package"""
    return functools.partial(names, package)


def run_interactive(package: str, action: str, *args: Any, **_kwargs: Any) -> Any:
    """Call the given action's run"""
    action_cls = get(package, action)
    app, interaction = args
    app_action = action_cls(app.args)
    supports_interactive = hasattr(app_action, "run")
    if not supports_interactive:
        logger.error("Subcommand '%s' does not support mode interactive", action)
    run_action = app_action.run if supports_interactive else app_action.no_interactive_mode
    return run_action(app=app, interaction=interaction)


def run_interactive_factory(package: str) -> Callable:
    """Create a call() function for one package"""
    return functools.partial(run_interactive, package)


def run_stdout(package: str, action: str, *args: Any, **_kwargs: Any) -> Any:
    """Call the given action's run_stdout"""
    action_cls = get(package, action)
    args = args[0]
    return action_cls(args).run_stdout()


def run_stdout_factory(package: str) -> Callable:
    """Create a run_stdout() function for one package"""
    return functools.partial(run_stdout, package)
