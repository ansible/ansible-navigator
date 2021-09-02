""" Some action stuff """


import functools
import importlib
import re
from collections import namedtuple

from typing import Any
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources  # type: ignore


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
    files = resources.contents(package)  # type: ignore
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
    """Return a tuple of tuples, anem, kegex"""
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
    return action_cls(app.args).run(app=app, interaction=interaction)


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
