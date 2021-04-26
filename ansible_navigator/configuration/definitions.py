from enum import Enum

from types import SimpleNamespace

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Union

from ansible_navigator.utils import Sentinel
from ansible_navigator.utils import oxfordcomma


class CliParameters(SimpleNamespace):
    """a structure to hold the cli param"""

    action: Union[None, str] = None
    long_override: Union[None, str] = None
    nargs: Union[None, Dict] = None
    positional: bool = False
    short: Union[None, str] = None


class EntrySource(Enum):
    """mapping some enums to log friendly text"""

    DEFAULT_CFG = "default configuration value"
    ENVIRONMENT_VARIABLE = "environemnt variable"
    PREVIOUS_CLI = "previous cli command"
    USER_CFG = "user provided configuration file"
    USER_CLI = "cli parameters"


class EntryValue(SimpleNamespace):
    """A structure to store a value"""

    default: Any = Sentinel
    current: Any = Sentinel
    source: Union[EntrySource, Sentinel] = Sentinel


class Entry(SimpleNamespace):
    # pylint: disable=inherit-non-class
    # pylint: disable=too-few-public-methods
    """One entry in the configuration"""

    name: str
    description: str
    settings_file_path: str
    value: EntryValue

    choices: List = []
    cli_parameters: Union[None, CliParameters] = None
    environment_variable_override: Union[None, str] = None
    internal: bool = False
    settings_file_path_override: Union[None, str] = None
    subcommands: List[str] = []

    def environment_variable(self, prefix):
        if self.environment_variable_override is not None:
            envvar = f"{prefix}_{self.environment_variable}"
        else:
            envvar = f"{prefix}_{self.name.replace('--', '')}"
        envvar = envvar.replace("-", "_").upper()
        return envvar

    @property
    def invalid_choice(self):
        name = self.name.replace("_", "-")
        msg = (
            f"{name} must be one of "
            + oxfordcomma(self.choices, "or")
            + f", but set as '{self.value.current}' in "
            + self.value.source.value
        )
        return msg

    @property
    def name_dashed(self):
        return self.name.replace("_", "-")

    def settings_file_path(self, prefix):
        if self.settings_file_path_override is not None:
            sfp = f"{prefix}.{self.settings_file_path_override}"
        else:
            sfp = f"{prefix}.{self.name.replace('_', '-')}"
        return sfp


class SubCommand(SimpleNamespace):
    name: str
    description: str


class Config(SimpleNamespace):
    """the main object for storing an application config"""

    application_name: str
    entries: List[Entry]
    subcommands: List[SubCommand]
    post_processor = Callable

    initial: Any = None

    def __getattribute__(self, attr):
        """Returns the respective item."""
        try:
            found_entry = [entry for entry in super().__getattribute__("entries") if entry.name == attr]
            if found_entry:
                return found_entry[0].value.current
        except AttributeError:
            pass
        return super().__getattribute__(attr)

    def entry(self, name):
        """retrieve a configuration entry by name"""
        found_entry = [entry for entry in self.entries if entry.name == name]
        return found_entry[0]


class Message(NamedTuple):
    log_level: str
    message: str
