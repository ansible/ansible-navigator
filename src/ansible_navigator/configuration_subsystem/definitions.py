"""configuration definitions
"""
from enum import Enum
from types import SimpleNamespace
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

from ..utils import oxfordcomma


class CliParameters(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """An object to hold the CLI parameters"""

    action: Union[None, str] = None
    long_override: Union[None, str] = None
    nargs: Union[None, Dict] = None
    positional: bool = False
    short: Union[None, str] = None
    metavar: Union[None, str] = None


class Constants(Enum):
    """Mapping some constants to friendly text"""

    ALL = "All the things"
    DEFAULT_CFG = "default configuration value"
    ENVIRONMENT_VARIABLE = "environment variable"
    NONE = "None of the things"
    NOT_SET = "value has not been set"
    PREVIOUS_CLI = "previous cli command"
    SAME_SUBCOMMAND = (
        "used to determine if an entry should be used when"
        " applying previous cli common entries, this indicates"
        " that it will only be used if the subcommand is the same"
    )
    SEARCH_PATH = "Found using search path"
    SENTINEL = "indicates a nonvalue"
    USER_CFG = "user provided configuration file"
    USER_CLI = "cli parameters"


class SettingsEntryValue(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """An object to store a value"""

    default: Any = Constants.NOT_SET
    current: Any = Constants.NOT_SET
    source: Constants = Constants.NOT_SET


class SettingsEntry(SimpleNamespace):
    """One entry in the configuration

    apply_to_subsequent_cli: Should this be applied to future CLIs parsed
    choice: valid choices for this entry
    cli_parameters: argparse specific params
    delay_post_process: Post process in normal (alphabetical) order or wait until after first pass?
    environment_variable_override: override the default environment variable
    name: the reference name for the entry
    settings_file_path_override: over the default settings file path
    short_description: A short description used for the argparse help
    subcommand_value: Does the hold the names of the subcommand
    subcommands: which subcommand should this be used for
    value: the SettingsEntryValue for the entry
    """

    name: str
    short_description: str
    value: SettingsEntryValue

    apply_to_subsequent_cli: Constants = Constants.ALL
    change_after_initial: bool = True
    choices: List = []
    cli_parameters: Union[None, CliParameters] = None
    delay_post_process: bool = False
    environment_variable_override: Union[None, str] = None
    settings_file_path_override: Union[None, str] = None
    subcommands: Union[List[str], Constants] = Constants.ALL
    subcommand_value: bool = False

    def environment_variable(self, prefix: str = "") -> str:
        """Generate an effective environment variable for this entry"""
        if self.environment_variable_override is not None:
            envvar = self.environment_variable_override
        else:
            envvar = f"{prefix}_{self.name.replace('--', '')}"
        envvar = envvar.replace("-", "_").upper()
        return envvar

    @property
    def invalid_choice(self) -> str:
        """Generate an invalid choice message for this entry"""
        name = self.name.replace("_", "-")
        if self.value.source is not Constants.NOT_SET:
            choices = [str(choice).lower() for choice in self.choices]
            msg = (
                f"{name} must be one of "
                + oxfordcomma(choices, "or")
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
            sfp = f"{prefix}.{self.name}"
        return sfp.replace("_", "-")


class SubCommand(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """An object to hold a subcommand"""

    name: str
    description: str
    epilog: Union[None, str] = None


class ApplicationConfiguration(SimpleNamespace):
    """The main object for storing an application config"""

    application_name: str = ""
    entries: List[SettingsEntry] = []
    internals: SimpleNamespace
    subcommands: List[SubCommand]
    post_processor = Callable
    initial: Any = None
    original_command: List[str]

    def _get_by_name(self, name, kind):
        try:
            return next(entry for entry in super().__getattribute__(kind) if entry.name == name)
        except StopIteration as exc:
            raise KeyError(name) from exc

    def __getattribute__(self, attr: str) -> Any:
        """Returns a matching entry or the default from super"""
        try:
            return super().__getattribute__("_get_by_name")(attr, "entries").value.current
        except KeyError:
            return super().__getattribute__(attr)

    def entry(self, name) -> SettingsEntry:
        """Retrieve a configuration entry by name"""
        return self._get_by_name(name, "entries")

    def subcommand(self, name) -> SubCommand:
        """Retrieve a configuration subcommand by name"""
        return self._get_by_name(name, "subcommands")
