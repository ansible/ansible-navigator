"""Configuration definitions."""
from __future__ import annotations

import copy
import re

from collections.abc import Iterable
from dataclasses import InitVar
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import NewType
from typing import TypeVar
from typing import Union

from ansible_navigator.utils.functions import abs_user_path
from ansible_navigator.utils.functions import oxfordcomma


if TYPE_CHECKING:
    from .navigator_configuration import Internals
    from .navigator_post_processor import NavigatorPostProcessor


def version_added_sanity_check(version: str):
    """Check if a version string is valid.

    :param version: The version string to check
    :raises AssertionError: If the version string is invalid
    """
    re_version = re.compile(r"^v\d+\.\d+$")
    assert re_version.match(version) is not None, "Version must be in the form of v{major}.{minor}"


class Constants(Enum):
    """Mapping some constants to friendly text."""

    ALL = "All"
    ANSIBLE_CFG = "Ansible configuration file"
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
    SEARCH_PATH = "Search path"
    SENTINEL = "Indicates a non value"
    TEST = "Indicates a value set from a test"
    USER_CFG = "Settings file"
    USER_CLI = "Command line"

    def __str__(self) -> str:
        """Use the value when presented as a string.

        :returns: The value as type str
        """
        return str(self.value)


# The following are ordered to build up to an ApplicationConfiguration


@dataclass
class CliParameters:
    """An object to hold the CLI parameters."""

    action: str | None = None
    const: bool | str | None = None
    long_override: str | None = None
    nargs: str | None = None
    positional: bool = False
    short: str | None = None
    metavar: str | None = None

    def long(self, name_dashed: str) -> str:
        """Provide a cli long parameter.

        :param name_dashed: The dashed name of the parent settings entry
        :returns: The long cli parameter
        """
        long = self.long_override or f"--{name_dashed}"
        return long


@dataclass
class SettingsEntryValue:
    """An object to store a value."""

    #: The default value for the entry
    default: Any = Constants.NOT_SET
    #: The current, effective value for the entry
    current: Any = Constants.NOT_SET
    #: Provide a specific default value to be used in the schema
    schema_default: str | Constants = Constants.NOT_SET
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
    #: Version added
    version_added: str
    #: Indicates if this should be applied to future CLIs parsed
    apply_to_subsequent_cli: Constants = Constants.ALL
    #: Indicates if this can be changed after initialization
    change_after_initial: bool = True
    #: The possible values for this entry
    choices: Iterable[bool | str] = field(default_factory=list)
    #: Argparse specific params
    cli_parameters: CliParameters | None = None
    #: Post process in normal (alphabetical) order or wait until after first pass
    delay_post_process: bool = False
    #: Override the default, generated environment variable
    environment_variable_override: str | None = None
    #: Over the default settings file path, dot delimited representation in tree
    environment_variable_split_char: str = ","
    #: The character used to split an environment variable value into a list
    settings_file_path_override: str | None = None
    #: Subcommand this should this be used for
    subcommands: list[str] | Constants = Constants.ALL
    #: Does this hold the name of the active subcommand
    subcommand_value: bool = False

    def __post_init__(self):
        """Perform post initialization actions."""
        version_added_sanity_check(self.version_added)

    def environment_variable(self, prefix: str = "") -> str:
        """Generate an effective environment variable for this entry.

        :param prefix: The prefix for environmental variable
        :returns: Environmental variable with prefix prepended
        """
        if self.environment_variable_override is not None:
            env_var = self.environment_variable_override
        else:
            env_var = f"{prefix}_{self.name.replace('--', '')}"
        env_var = env_var.replace("-", "_").upper()
        return env_var

    @property
    def invalid_choice(self) -> str:
        """Generate an invalid choice message for this entry.

        :raises ValueError: If source is not set for that entry
        :returns: Constructed message
        """
        name = self.name.replace("_", "-")
        if self.value.source is Constants.NOT_SET:
            msg = f"Current source not set for {self.name}"
            raise ValueError(msg)

        choices = [str(choice).lower() for choice in self.choices]
        current = self.value.current
        if isinstance(current, list):
            choices_str = oxfordcomma(choices, "and/or")
            current = oxfordcomma(current, "and")
            prefix = f"The setting '{name}' must be one or more of"
        else:
            choices_str = oxfordcomma(choices, "or")
            prefix = f"The setting '{name}' must be one of"

        source = self.value.source.value
        msg = f"{prefix} {choices_str}, but set as '{current}'. ({source})"
        return msg

    @property
    def name_dashed(self) -> str:
        """Generate a dashed version of the name.

        :returns: Dashed version of the name
        """
        return self.name.replace("_", "-")

    def settings_file_path(self, prefix: str) -> str:
        """Generate an effective settings file path for this entry.

        :param prefix: The prefix for the settings file path
        :returns: Settings file path
        """
        prefix_str = f"{prefix}." if prefix else prefix

        if self.settings_file_path_override is not None:
            sfp = f"{prefix_str}{self.settings_file_path_override}"
        else:
            sfp = f"{prefix_str}{self.name}"

        return sfp.replace("_", "-")


@dataclass(frozen=True)
class SubCommand:
    """An object to hold a subcommand."""

    name: str
    description: str
    version_added: str
    epilog: str | None = None

    def __post_init__(self):
        """Perform post initialization actions."""
        version_added_sanity_check(self.version_added)


@dataclass
class ApplicationConfiguration:
    # pylint: disable=too-many-instance-attributes
    """The main object for storing an application config."""

    application_version: Constants | str
    entries: list[SettingsEntry]
    internals: Internals
    post_processor: NavigatorPostProcessor
    subcommands: list[SubCommand]

    application_name: str = ""
    original_command: list[str] = field(default_factory=list)

    initial: Any = None

    @property
    def application_name_dashed(self) -> str:
        """Generate a dashed version of the application name.

        :returns: Application name dashed
        """
        return self.application_name.replace("_", "-")

    def _get_by_name(self, name, kind):
        """Retrieve a settings entry by name.

        :param name: The name of the entry
        :param kind: The kind of entry to retrieve
        :returns: The settings entry
        :raises KeyError: If the entry is not found
        """
        try:
            return next(entry for entry in super().__getattribute__(kind) if entry.name == name)
        except StopIteration as exc:
            raise KeyError(name) from exc

    def __getattribute__(self, attr: str) -> Any:
        """Return a matching entry or the default from super.

        :param attr: The attribute to get
        :returns: Either the matching entry or default from super
        """
        try:
            return super().__getattribute__("_get_by_name")(attr, "entries").value.current
        except (AttributeError, KeyError):
            return super().__getattribute__(attr)

    def entry(self, name) -> SettingsEntry:
        """Retrieve a configuration entry by name.

        :param name: The name of the entry
        :returns: Configuration entry name
        """
        return self._get_by_name(name, "entries")

    def subcommand(self, name) -> SubCommand:
        """Retrieve a configuration subcommand by name.

        :param name: The name of the subcommand
        :returns: Configuration subcommand name
        """
        return self._get_by_name(name, "subcommands")


# The following are ordered to build up to an VolumeMount


class VolumeMountOption(Enum):
    """Options that can be tagged on to the end of volume mounts.

    Usually these are used for things like selinux relabeling, but there are
    some other valid options as well, which can and should be added here as
    needed. See ``man podman-run`` and ``man docker-run`` for valid choices and
    keep in mind that we support both runtimes.
    """

    # Overlay
    OVERLAY = "O"

    # Read Only
    ro = "ro"

    # Read Write
    rw = "rw"

    # Relabel as private
    Z = "Z"

    # Relabel as shared.
    z = "z"


V = TypeVar("V", bound="VolumeMount")


class VolumeMountError(Exception):
    """Custom exception raised when building VolumeMounts."""


@dataclass(frozen=True)
class VolumeMount:
    """Describes EE volume mounts."""

    fs_source: str
    """The source file system path of the volume mount"""
    fs_destination: str
    """The destination file system path in the container for the volume mount"""
    settings_entry: str
    """The name of the settings entry requiring this volume mount"""
    source: Constants = field(compare=False)
    """The settings source for this volume mount"""
    options_string: InitVar[str]
    """Comma delimited options"""
    options: tuple[VolumeMountOption, ...] = ()
    """Options for the bind mount"""

    def __post_init__(self, options_string):
        """Post process the ``VolumeMount`` and perform sanity checks.

        :raises VolumeMountError: When a viable VolumeMount cannot be created
        :param options_string: Option entries in as type string
        """
        errors = []

        # Ensure each is a string
        if not isinstance(self.fs_source, str):
            errors.append(f"Source: '{self.fs_source}' is not a string.")
        if not isinstance(self.fs_destination, str):
            errors.append(f"Destination: '{self.fs_destination}' is not a string.")
        if not isinstance(options_string, str):
            errors.append(f"Options: '{options_string}' is not a string.")

        # Ensure source and dest are not empty
        if self.fs_source == "":
            errors.append("Source not provided.")
        if self.fs_destination == "":
            errors.append("Destination not provided.")

        # Exit early for errors
        if errors:
            raise VolumeMountError(" ".join(errors))

        # Resolve the source and destination
        # frozen, cannot use simple assignment to initialize fields, and must use:
        object.__setattr__(self, "fs_source", abs_user_path(self.fs_source))
        object.__setattr__(self, "fs_destination", abs_user_path(self.fs_destination))

        # Source must exist
        if not Path(self.fs_source).exists():
            error_msg = f"Source: '{self.fs_source}' does not exist."
            raise VolumeMountError(error_msg)

        # Validate and populate _options
        if options_string == "":
            return

        options = []
        option_values = [o.value for o in VolumeMountOption]
        for option in options_string.split(","):
            if option not in option_values:
                errors.append(
                    f"Unrecognized option: '{option}',"
                    f" available options include"
                    f" {oxfordcomma(option_values, condition='and/or')}.",
                )
            else:
                options.append(VolumeMountOption(option))

        if errors:
            raise VolumeMountError(" ".join(errors))

        unique = sorted(set(options), key=options.index)
        object.__setattr__(self, "options", tuple(unique))

    def to_string(self) -> str:
        """Render the volume mount in a way that (docker|podman) understands.

        :returns: File system source and system path for volume mount
        """
        out = f"{self.fs_source}:{self.fs_destination}"
        if self.options:
            joined_opts = ",".join(o.value for o in self.options)
            out += f":{joined_opts}"
        return out


# The following are ordered to build up to a Mode


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


@dataclass
class PaeChangeRequest:
    """Data structure to hold playbook artifact change request by a settings entry."""

    entry: str
    """The entry making the request"""
    playbook_artifact_enable: bool
    """The desired value for playbook_artifact_enable"""


# and some common ones

# A type used for the settings as a dictionary
SettingsFileType = NewType("SettingsFileType", dict[str, Union[bool, dict, int, str, list]])

# A type used to describe a schema file for the settings
SettingsSchemaType = NewType(
    "SettingsSchemaType",
    dict[str, dict[str, Union[bool, dict, int, str, list]]],
)
