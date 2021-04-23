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
    environment_variable_override: Union[None, str] = None
    post_process: Union[None, Callable] = None
    internal: bool = False
    settings_file_path_override: Union[None, str] = None
    subcommands: List[str] = []

    def environment_variable(self, prefix):
        if self.environment_variable_override is not None:
            envvar = f"{prefix}_{self.environment_variable}"
        else:
            envvar = f"{prefix}_{self.cli_parameters.long.replace('--', '')}"
        envvar = envvar.replace('-', '_').upper()
        return envvar


    @property
    def invalid_choice(self):
        name = self.name.replace('_', "-")
        msg = (f"{name} must be one of " +
                oxfordcomma(self.choices, "or") +
                f", but set as '{self.value.current}' in " +
                self.value.source.value)  
        return msg
    
    @property
    def name_dashed(self):
        return self.name.replace("_", "-")
 
    def settings_file_path(self, prefix):
        if self.settings_file_path_override is not None:
            sfp = f"{prefix}.{self.settings_file_path_override}"
        else:
            sfp = f"{prefix}.{self.cli_parameters.long.replace('--', '')}"
        return sfp


class EntrySource(Enum):
    """mapping some enums to log friendly text"""

    DEFAULT_CFG = "default configuration value"
    ENVIRONMENT_VARIABLE = "environemnt variable"
    USER_CFG = "user provided configuration file"
    USER_CLI = "cli parameters"


class SubCommand(SimpleNamespace):
    name: str
    description: str


class Config(SimpleNamespace):
    """the main object for storing an application config"""

    entries: List[Entry]
    initial: Any = None
    application_name: str
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
