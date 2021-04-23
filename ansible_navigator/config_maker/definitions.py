from enum import Enum

from types import SimpleNamespace

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union

from ansible_navigator.utils import Sentinel


class CliParameters(SimpleNamespace):
    """a structure to hold the cli param"""

    short: str
    long: str


class EntryValue(SimpleNamespace):
    """A structure to store a value"""

    default: Any
    current: Any = Sentinel
    source: Any = Sentinel


class Entry(SimpleNamespace):
    # pylint: disable=inherit-non-class
    # pylint: disable=too-few-public-methods
    """One entry in the configuration"""

    name: str
    cli_parameters: CliParameters
    description: str
    settings_file_path: str
    value: EntryValue

    argparse_params: Dict = {}
    choices: List = []
    post_process: Union[None, Callable] = None
    internal: bool = False
    settings_file_path: Union[None, str] = None

    subcommands: List[str] = []


class EntrySource(Enum):
    """mapping some enums to log friendly text"""

    USER_CFG = "user provided configuration file"
    USER_CLI = "user provided at cli"
    DEFAULT_CFG = "default configuration value"


class SubCommand(SimpleNamespace):
    name: str
    description: str


class Config(SimpleNamespace):
    """the main object for storing an application config"""

    entries: List[Entry]
    initial: Any = None
    root_settings_key: str
    subcommands: List[SubCommand]

    def __getattribute__(self, attr):
        # pylint: disable=raise-missing-from
        """Returns the respective item."""
        try:
            return object.__getattribute__(self, attr)
        except AttributeError as exc:
            found_entry = [entry for entry in self.entries if entry.name == attr]
            if len(found_entry) > 1:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has multiple attributes '{attr}'"
                )
            if not found_entry:
                raise exc
            return found_entry[0].value.current

    def entry(self, name):
        """retrieve a configuration entry by name"""
        found_entry = [entry for entry in self.entries if entry.name == name]
        if len(found_entry) > 1:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has multiple attributes '{name}'"
            )
        if not found_entry:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return found_entry[0]


class Message(NamedTuple):
    log_level: str
    message: str
