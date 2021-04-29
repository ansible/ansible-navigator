""" cofiguration definitions
"""
from enum import Enum

from types import SimpleNamespace

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Type
from typing import Union

from ..utils import Sentinel
from ..utils import oxfordcomma


class CliParameters(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """An object to hold the cli parameters"""

    action: Union[None, str] = None
    long_override: Union[None, str] = None
    nargs: Union[None, Dict] = None
    positional: bool = False
    short: Union[None, str] = None


class EntrySource(Enum):
    """Mapping some enums to log friendly text"""

    DEFAULT_CFG = "default configuration value"
    ENVIRONMENT_VARIABLE = "environemnt variable"
    PREVIOUS_CLI = "previous cli command"
    USER_CFG = "user provided configuration file"
    USER_CLI = "cli parameters"


class EntryValue(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """An object to store a value"""

    default: Any = Sentinel
    current: Any = Sentinel
    source: Union[EntrySource, Type[Sentinel]] = Sentinel


class Entry(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """One entry in the configuration"""

    name: str
    short_description: str
    value: EntryValue

    choices: List = []
    cli_parameters: Union[None, CliParameters] = None
    environment_variable_override: Union[None, str] = None
    internal: bool = False
    settings_file_path_override: Union[None, str] = None
    subcommands: List[str] = []
    subcommand_value: bool = False

    def environment_variable(self, prefix: str) -> str:
        """Generate an effective environment variable for this entry"""
        if self.environment_variable_override is not None:
            envvar = f"{prefix}_{self.environment_variable_override}"
        else:
            envvar = f"{prefix}_{self.name.replace('--', '')}"
        envvar = envvar.replace("-", "_").upper()
        return envvar

    @property
    def invalid_choice(self) -> str:
        """Generate an invalid choice message for this entry"""
        name = self.name.replace("_", "-")
        if isinstance(self.value.source, EntrySource):
            msg = (
                f"{name} must be one of "
                + oxfordcomma(self.choices, "or")
                + f", but set as '{self.value.current}' in "
                + self.value.source.value
            )
            return msg
        raise ValueError(f"Current source not set for {self.name}")

    @property
    def name_dashed(self) -> str:
        """Generate a dashed version of the name"""
        return self.name.replace("_", "-")

    def settings_file_path(self, prefix: str) -> str:
        """Generate an effective settings file path for this entry"""
        if self.settings_file_path_override is not None:
            sfp = f"{prefix}.{self.settings_file_path_override}"
        else:
            sfp = f"{prefix}.{self.name.replace('_', '-')}"
        return sfp


class SubCommand(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """An object to hold a subcommand"""

    name: str
    description: str


class ApplicationConfiguration(SimpleNamespace):
    """The main object for storing an application config"""

    application_name: str
    entries: List[Entry]
    subcommands: List[SubCommand]
    post_processor = Callable

    initial: Any = None

    def __getattribute__(self, attr: str) -> Any:
        """Returns a matching entry or the default bwo super"""
        try:
            found_entry = [
                entry for entry in super().__getattribute__("entries") if entry.name == attr
            ]
            if found_entry:
                return found_entry[0].value.current
        except AttributeError:
            pass
        return super().__getattribute__(attr)

    def entry(self, name) -> Entry:
        """Retrieve a configuration entry by name"""
        found_entry = [entry for entry in self.entries if entry.name == name]
        return found_entry[0]


class Message(NamedTuple):
    """An object ot hold a message"""

    log_level: str
    message: str
