"""configuration definitions
"""

import copy

from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from itertools import chain
from itertools import repeat
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from ..utils.functions import oxfordcomma


if TYPE_CHECKING:
    from .navigator_configuration import Internals
    from .navigator_post_processor import NavigatorPostProcessor


@dataclass
class CliParameters:
    """An object to hold the CLI parameters."""

    action: Optional[str] = None
    long_override: Optional[str] = None
    nargs: Optional[str] = None
    positional: bool = False
    short: Optional[str] = None
    metavar: Optional[str] = None

    def long(self, name_dashed: str) -> str:
        """Provide a cli long parameter.

        :param name_dashed: The dashed name of the parent settings entry
        :returns: The long cli parameter
        """
        long = self.long_override or f"--{name_dashed}"
        return long


class Constants(Enum):
    """Mapping some constants to friendly text"""

    ALL = "All"
    AUTO = "Automatically determined"
    DEFAULT_CFG = "Defaults"
    ENVIRONMENT_VARIABLE = "Environment variable"
    NONE = "None"
    NOT_SET = "Not set"
    PREVIOUS_CLI = "Previous cli command"
    SAME_SUBCOMMAND = (
        "Used to determine if an entry should be used when"
        " applying previous cli common entries, this indicates"
        " that it will only be used if the subcommand is the same"
    )
    SEARCH_PATH = "Found using search path"
    SENTINEL = "Indicates a nonvalue"
    USER_CFG = "User-provided configuration file"
    USER_CLI = "Provided at command line"


@dataclass
class SettingsEntryValue:
    """An object to store a value."""

    #: The default value for the entry
    default: Any = Constants.NOT_SET
    #: The current, effective value for the entry
    current: Any = Constants.NOT_SET
    #: Indicates where the current value came from
    source: Constants = Constants.NOT_SET

    @property
    def is_default(self):
        """Determine if the current value is the default value.

        :returns: Indication of if the current is the default
        """
        result = self.default == self.current
        return result

    @property
    def resolved(self):
        """Transform this entry to an entry without internal constants.

        This would typically be used when the attributes need to be presented to the user.
        Constants are resolved to their value.

        :returns: An entry without internal constants for attributes
        """
        new_entry = copy.deepcopy(self)

        if isinstance(self.current, Constants):
            new_entry.current = self.current.value

        if isinstance(self.default, Constants):
            new_entry.default = self.default.value

        return new_entry


@dataclass
class SettingsEntry:
    # pylint: disable=too-many-instance-attributes
    """One entry in the configuration."""

    #: The reference name for the entry
    name: str
    #: A short description used for the argparse help
    short_description: str
    #: The value for the entry
    value: SettingsEntryValue
    #: Indicates if this should be applied to future CLIs parsed
    apply_to_subsequent_cli: Constants = Constants.ALL
    #: Indicates if this can be changed after initialization
    change_after_initial: bool = True
    #: The possible values for this entry
    choices: Iterable[Union[bool, str]] = field(default_factory=list)
    #: Argparse specific params
    cli_parameters: Optional[CliParameters] = None
    #: Post process in normal (alphabetical) order or wait until after first pass
    delay_post_process: bool = False
    #: Override the default, generated environment variable
    environment_variable_override: Optional[str] = None
    #: Over the default settings file path, dot delimited representation in tree
    settings_file_path_override: Optional[str] = None
    #: Subcommand this should this be used for
    subcommands: Union[List[str], Constants] = Constants.ALL
    #: Does this hold the name of the active subcommand
    subcommand_value: bool = False

    def environment_variable(self, prefix: str = "") -> str:
        """Generate an effective environment variable for this entry"""
        if self.environment_variable_override is not None:
            env_var = self.environment_variable_override
        else:
            env_var = f"{prefix}_{self.name.replace('--', '')}"
        env_var = env_var.replace("-", "_").upper()
        return env_var

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
        if prefix:
            prefix_str = f"{prefix}."
        else:
            prefix_str = prefix

        if self.settings_file_path_override is not None:
            sfp = f"{prefix_str}{self.settings_file_path_override}"
        else:
            sfp = f"{prefix_str}{self.name}"

        return sfp.replace("_", "-")


@dataclass(frozen=True)
class SubCommand:
    """An object to hold a subcommand"""

    name: str
    description: str
    epilog: Optional[str] = None


@dataclass
class ApplicationConfiguration:
    # pylint: disable=too-many-instance-attributes
    """The main object for storing an application config"""

    application_version: Union[Constants, str]
    entries: List[SettingsEntry]
    internals: "Internals"
    post_processor: "NavigatorPostProcessor"
    subcommands: List[SubCommand]

    application_name: str = ""
    original_command: List[str] = field(default_factory=list)

    initial: Any = None

    @property
    def application_name_dashed(self) -> str:
        """Generate a dashed version of the application name"""
        return self.application_name.replace("_", "-")

    def _get_by_name(self, name, kind):
        try:
            return next(entry for entry in super().__getattribute__(kind) if entry.name == name)
        except StopIteration as exc:
            raise KeyError(name) from exc

    def __getattribute__(self, attr: str) -> Any:
        """Returns a matching entry or the default from super"""
        try:
            return super().__getattribute__("_get_by_name")(attr, "entries").value.current
        except (AttributeError, KeyError):
            return super().__getattribute__(attr)

    def entry(self, name) -> SettingsEntry:
        """Retrieve a configuration entry by name"""
        return self._get_by_name(name, "entries")

    def subcommand(self, name) -> SubCommand:
        """Retrieve a configuration subcommand by name"""
        return self._get_by_name(name, "subcommands")


class VolumeMountOption(Enum):
    """Options that can be tagged on to the end of volume mounts.

    Usually these are used for things like selinux relabeling, but there are
    some other valid options as well, which can and should be added here as
    needed. See ``man podman-run`` and ``man docker-run`` for valid choices and
    keep in mind that we support both runtimes.
    """

    # Relabel as private
    Z = "Z"

    # Relabel as shared.
    z = "z"  # pylint: disable=invalid-name


V = TypeVar("V", bound="VolumeMount")  # pylint: disable=invalid-name


@dataclass
class VolumeMount:
    """Describes EE volume mounts."""

    fs_destination: str
    """The destination file system path in the container for the volume mount"""
    fs_source: str
    """The source file system path of the volume mount"""
    settings_entry: str
    """The name of the settings entry requiring this volume mount"""
    source: Constants
    """The settings source for this volume mount"""
    options: List[VolumeMountOption] = field(default_factory=list)
    """Options for the bind mount"""

    def exists(self) -> bool:
        """Determine if the volume mount source exists."""
        return Path(self.fs_source).exists()

    def to_string(self) -> str:
        """Render the volume mount in a way that (docker|podman) understands."""
        out = f"{self.fs_source}:{self.fs_destination}"
        if self.options:
            joined_opts = ",".join(o.value for o in self.options)
            out += f":{joined_opts}"
        return out

    @classmethod
    def from_string(cls: Type[V], settings_entry: str, source: Constants, string: str) -> V:
        """Create a ``VolumeMount`` from a string.

        :param settings_entry: The settings entry
        :param source: The source of the string
        :param string: The string from which the volume mount will be created
        :raises ValueError: When source or destination are missing, or unrecognized label
        :returns: A populated volume mount
        """
        fs_source, fs_destination, options, *left_overs = chain(string.split(":"), repeat("", 3))
        if options:
            option_list = [
                const
                for const in VolumeMountOption
                for option in options.split(",")
                if const.value == option
            ]
        unrecognized_label = len(options.split(",")) != len(option_list)

        if any(left_overs):
            raise ValueError("Not formatted correctly")
        if unrecognized_label:
            raise ValueError("Unrecognized label in volume mount string")
        if not fs_source:
            raise ValueError("Could not extract source from string")
        if not fs_destination:
            raise ValueError("Could not extract destination from string")
        return cls(
            fs_source=fs_source,
            fs_destination=fs_destination,
            options=option_list,
            settings_entry=settings_entry,
            source=source,
        )

    @classmethod
    def from_dictionary(
        cls: Type[V],
        settings_entry: str,
        source: Constants,
        dictionary: dict,
    ) -> V:
        """Create a ``VolumeMount`` from a dictionary.

        :param dictionary: The dictionary from which the volume mount will be created
        :param settings_entry: The settings entry
        :param source: The source of the string
        :raises ValueError: When source or destination are missing, or unrecognized label
        :returns: A populated volume mount
        """
        options = dictionary.get("label", "")
        if options:
            option_list = [
                const
                for const in VolumeMountOption
                for option in options.split(",")
                if const.value == option
            ]
        unrecognized_label = len(options.split(",")) != len(option_list)
        if unrecognized_label:
            raise ValueError("Unrecognized labe in volume mount string")
        try:
            return cls(
                fs_source=dictionary["src"],
                fs_destination=dictionary["dest"],
                options=option_list,
                settings_entry=settings_entry,
                source=source,
            )
        except KeyError as exc:
            raise ValueError("Source or destination missing") from exc
        except TypeError as exc:
            raise ValueError("Not a dictionary") from exc


class Mode(Enum):
    """An enum to restrict mode type."""

    STDOUT: str = "stdout"
    INTERACTIVE: str = "interactive"


@dataclass
class ModeChangeRequest:
    """Data structure to contain a mode change request by a settings entry."""

    entry: str
    """The entry making the request"""
    mode: Mode
    """The desired mode"""
