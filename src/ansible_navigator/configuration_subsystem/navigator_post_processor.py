"""post processing of ansible-navigator configuration
"""
import importlib
import logging
import os
import shlex
import shutil

from functools import partialmethod
from itertools import chain
from itertools import repeat
from pathlib import Path
from string import Formatter
from typing import List
from typing import Tuple

from ..utils.compatibility import zoneinfo
from ..utils.functions import ExitMessage
from ..utils.functions import ExitPrefix
from ..utils.functions import LogMessage
from ..utils.functions import abs_user_path
from ..utils.functions import check_for_ansible
from ..utils.functions import flatten_list
from ..utils.functions import oxfordcomma
from ..utils.functions import str2bool
from ..utils.functions import to_list
from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Constants as C
from .definitions import Mode
from .definitions import ModeChangeRequest
from .definitions import SettingsEntry
from .definitions import VolumeMount
from .definitions import VolumeMountError


def _post_processor(func):
    def wrapper(*args, **kwargs):
        name = kwargs["entry"].name
        before = str(kwargs["entry"].value.current)
        messages, exit_messages = func(*args, **kwargs)
        after = str(kwargs["entry"].value.current)
        changed = before != after
        messages.append(
            LogMessage(
                level=logging.DEBUG,
                message=f"Completed post processing for {name}. (changed={changed})",
            ),
        )
        if changed:
            messages.append(LogMessage(level=logging.DEBUG, message=f" before: '{before}'"))
            messages.append(LogMessage(level=logging.DEBUG, message=f" after: '{after}'"))
        return messages, exit_messages

    return wrapper


PostProcessorReturn = Tuple[List[LogMessage], List[ExitMessage]]


class NavigatorPostProcessor:
    # pylint:disable=too-many-public-methods
    """application post processor"""

    def __init__(self):
        """Initialize the post processor."""
        #: Volume mounts accumulated from post processing various config entries.
        #: These get processed towards the end, in the (delayed)
        #: :meth:`.execution_environment_volume_mounts` post-processor.
        self.extra_volume_mounts: List[VolumeMount] = []
        self._requested_mode: List[ModeChangeRequest] = []

    @staticmethod
    def _true_or_false(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        try:
            entry.value.current = str2bool(entry.value.current)
        except ValueError:
            exit_msg = f"{entry.name} could not be converted to a boolean value,"
            exit_msg += f" value was '{entry.value.current}' ({type(entry.value.current).__name__})"
            exit_messages.append(ExitMessage(message=exit_msg))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def ansible_runner_artifact_dir(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process ansible_runner_artifact_dir path"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def ansible_runner_rotate_artifacts_count(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process ansible_runner_rotate_artifacts_count"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            try:
                entry.value.current = int(entry.value.current)
            except ValueError as exc:
                exit_msg = f"Value should be valid integer. Failed with error {str(exc)}"
                exit_messages.append(ExitMessage(message=exit_msg))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def ansible_runner_timeout(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process ansible_runner_timeout"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            try:
                entry.value.current = int(entry.value.current)
            except ValueError as exc:
                exit_msg = f"Value should be valid integer. Failed with error {str(exc)}"
                exit_messages.append(ExitMessage(message=exit_msg))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def collection_doc_cache_path(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process collection doc cache path"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def cmdline(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process cmdline"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if isinstance(entry.value.current, str):
            entry.value.current = shlex.split(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def container_engine(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process container_engine"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current == "auto":
            choices = filter(lambda x: x != "auto", entry.choices)
            for choice in choices:
                if shutil.which(str(choice)):
                    entry.value.current = choice
                    entry.value.source = C.AUTO
                    break
        return messages, exit_messages

    @_post_processor
    def display_color(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process display_color"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = False
            message = f"{entry.environment_variable()} was set, set to {entry.value.current}"
            messages.append(LogMessage(level=logging.INFO, message=message))
            return messages, exit_messages
        return self._true_or_false(entry, config)

    @_post_processor
    def editor_console(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process editor_console"""
        return self._true_or_false(entry, config)

    @_post_processor
    def execution_environment(self, entry: SettingsEntry, config) -> PostProcessorReturn:
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        """Post process execution_environment"""
        messages, exit_messages = self._true_or_false(entry, config)
        if entry.value.current is True:
            exit_msg = ""
            if config.container_engine == "auto":
                exit_msg = "No container engine could be found:"
            else:
                container_engine_location = shutil.which(config.container_engine)
                if container_engine_location is None:
                    exit_msg = "The specified container engine could not be found:"
            if exit_msg:
                exit_msg += f" '{config.container_engine}',"
                exit_msg += f" set by '{config.entry('container_engine').value.source.value}'"
                exit_messages.append(ExitMessage(message=exit_msg))
                ce_short = config.entry("container_engine").cli_parameters.short
                if isinstance(entry.cli_parameters, CliParameters):
                    entry_short = entry.cli_parameters.short
                else:
                    entry_short = None
                choices = config.entry("container_engine").choices
                if ce_short and entry_short:
                    hint = ""
                    if config.container_engine == "auto":
                        ce_choices = filter(lambda x: x != "auto", choices)
                        hint = f"Try installing {oxfordcomma(ce_choices, 'or')}"
                    elif config.container_engine in choices:
                        alternatives = filter(lambda x: x != config.container_engine, choices)
                        other = [f"{ce_short} {alt}" for alt in alternatives]
                        hint = f"Try installing '{config.container_engine}'"
                        hint += f", try again with {oxfordcomma(other, 'or')}"
                        hint += (
                            f" or even '{entry_short}"
                            " false' to disable the use of an execution environment"
                        )
                    if hint:
                        exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))

            # check for ``/dev/mqueue/`` when using podman because runner passes ipc=host
            # https://github.com/ansible/ansible-navigator/issues/610
            message_queue_path = "/dev/mqueue/"
            podman_no_message_queue_dir = (
                config.container_engine == "podman" and not Path(message_queue_path).is_dir()
            )
            if podman_no_message_queue_dir:
                exit_msg = (
                    "Execution environment support while using podman requires a"
                    f" '{message_queue_path}' directory."
                )
                exit_messages.append(ExitMessage(message=exit_msg))
                hint = (
                    f"Try creating it with 'mkdir {message_queue_path}' or reference the"
                    " documentation for your operating system related to POSIX message queues."
                )
                exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))
        else:
            new_messages, new_exit_messages = check_for_ansible()
            messages.extend(new_messages)
            exit_messages.extend(new_exit_messages)

            if config.app == "exec" and isinstance(entry.cli_parameters, CliParameters):
                exit_msg = "The 'exec' subcommand requires execution environment support."
                exit_messages.append(ExitMessage(message=exit_msg))
                hint = (
                    f"Try again with '{entry.cli_parameters.short} true'"
                    " to enable the use of an execution environment."
                )
                exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))

        return messages, exit_messages

    @staticmethod
    @_post_processor
    def execution_environment_image(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process execution_environment_image"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if ":" not in entry.value.current:
            entry.value.current = f"{entry.value.current}:latest"
        return messages, exit_messages

    @_post_processor
    def execution_environment_volume_mounts(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process set_environment_variable.

        :param entry: The current settings entry
        :param config: The full application configuration
        :return: An instance of the standard post process return object
        """
        # pylint: disable=unused-argument
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals

        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        entry_name = entry.settings_file_path(prefix="")
        entry_source = entry.value.source
        volume_mounts: List[VolumeMount] = []

        if entry_source in (C.ENVIRONMENT_VARIABLE, C.USER_CLI):
            hint = (
                "Try again with format <source-path>:<destination-path>:<options>'."
                " Note: options is optional."
            )
            mount_strings = flatten_list(entry.value.current)
            for mount_str in mount_strings:
                src, dest, options, *left_overs = chain(mount_str.split(":"), repeat("", 3))
                if any(left_overs):
                    exit_msg = (
                        f"The following {entry_name} entry could not be parsed:"
                        f" {mount_str} ({entry_source.value})"
                    )
                    exit_messages.append(ExitMessage(message=exit_msg))
                    exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))

                try:
                    volume_mounts.append(
                        VolumeMount(
                            fs_source=src,
                            fs_destination=dest,
                            options_string=options,
                            settings_entry=entry_name,
                            source=entry_source,
                        ),
                    )
                except VolumeMountError as exc:
                    exit_msg = (
                        f"The following {entry_name} entry could not be parsed:"
                        f" {mount_str} ({entry.value.source.value}). Errors were found: {str(exc)}"
                    )
                    exit_messages.append(ExitMessage(message=exit_msg))
                    exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))

        elif entry.value.source is C.USER_CFG:
            hint = (
                "The value of execution-environment.volume-mounts should be a list"
                " of dictionaries and valid keys are 'src', 'dest' and 'options'."
            )
            if not isinstance(entry.value.current, list):
                exit_msg = f"{entry_name} entries could not be parsed. ({entry_source.value})"
                exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = hint
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            else:
                for volume_mount in entry.value.current:
                    try:
                        volume_mounts.append(
                            VolumeMount(
                                fs_source=volume_mount.get("src"),
                                fs_destination=volume_mount.get("dest"),
                                options_string=volume_mount.get("options", ""),
                                settings_entry=entry_name,
                                source=entry_source,
                            ),
                        )
                    except (AttributeError, VolumeMountError) as exc:
                        exit_msg = (
                            f"The following {entry_name} entry could not be parsed:  {volume_mount}"
                            f" ({entry_source.value}). Errors were found: {str(exc)}"
                        )
                        exit_messages.append(ExitMessage(message=exit_msg))
                        exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))

        # Get out fast if we had any errors
        if exit_messages:
            return messages, exit_messages

        # New mounts were provided
        if volume_mounts:
            entry.value.current = [v.to_string() for v in volume_mounts]

        # Extra mounts were requested, these get added to either
        # new_mounts, C.PREVIOUS_CLI or C.NOT_SET
        if self.extra_volume_mounts:
            if not isinstance(entry.value.current, list):
                entry.value.current = []
            entry.value.current.extend(v.to_string() for v in self.extra_volume_mounts)

        # Finally, ensure the list has no duplicates
        if isinstance(entry.value.current, list):
            entry.value.current = sorted(set(entry.value.current), key=entry.value.current.index)

        return messages, exit_messages

    @staticmethod
    @_post_processor
    def container_options(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process container_options"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = to_list(entry.value.current)
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    @_post_processor
    def exec_shell(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process ``exec_shell``.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        return self._true_or_false(entry, config)

    @_post_processor
    def _forced_stdout(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
        subcommand: str,
    ) -> PostProcessorReturn:
        """Force mode stdout for a settings parameter.

        :param entry: The current settings entry
        :param config: The full application configuration
        :param subcommand: The applicable subcommand
        :returns: An instance of the standard post process return object
        """
        messages, exit_messages = self._true_or_false(entry, config)

        if entry.value.current is True and config.app == subcommand:
            mode = Mode.STDOUT
            self._requested_mode.append(ModeChangeRequest(entry=entry.name, mode=mode))
            message = message = f"`{entry.name} requesting mode {mode.value}"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        return messages, exit_messages

    help_builder = partialmethod(_forced_stdout, subcommand="builder")
    help_config = partialmethod(_forced_stdout, subcommand="config")
    help_doc = partialmethod(_forced_stdout, subcommand="doc")
    help_inventory = partialmethod(_forced_stdout, subcommand="inventory")
    help_playbook = partialmethod(_forced_stdout, subcommand="run")

    @_post_processor
    def images_details(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process execution_environment_image_details"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []

        entry.value.current = flatten_list(entry.value.current)
        # In the case --default was provided, set it to everything
        if not entry.value.current:
            entry.value.current = entry.value.default

        # Only force mode stdout if from the CLI so the values can be kept in settings
        # or in an environment variable and used with only --mode stdout
        if entry.value.source is C.USER_CLI:
            mode = Mode.STDOUT
            self._requested_mode.append(ModeChangeRequest(entry=entry.name, mode=mode))
            message = message = f"`{entry.name} requesting mode {mode.value}"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def inventory(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process inventory"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []

        if entry.value.current is C.NOT_SET:
            # Try the ansible.cfg file
            ansible_cfg = config.internals.ansible_configuration.contents
            if isinstance(ansible_cfg, dict):
                ansible_cfg_entry = ansible_cfg.get("defaults", {}).get("inventory")
                if isinstance(ansible_cfg_entry, str):
                    entry.value.current = [abs_user_path(i) for i in ansible_cfg_entry.split(",")]
                    entry.value.source = C.ANSIBLE_CFG
        else:
            # Use the specified
            flattened = flatten_list(entry.value.current)
            entry.value.current = []
            for inv_entry in flattened:
                if "," in inv_entry:
                    # host list
                    entry.value.current.append(inv_entry)
                else:
                    # file path
                    entry.value.current.append(abs_user_path(inv_entry))

        # Something may be required
        app_match = config.app == "inventory"
        current_not_set = entry.value.current is C.NOT_SET
        not_help_inventory = config.entry("help_inventory").value.current is False

        if app_match and current_not_set and not_help_inventory:
            exit_msg = "An inventory is required when using the inventory subcommand"
            exit_messages.append(ExitMessage(message=exit_msg))
            if entry.cli_parameters:
                exit_msg = f"Try again with '{entry.cli_parameters.short} <path to inventory>'"
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))

        return messages, exit_messages

    @staticmethod
    @_post_processor
    def inventory_column(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process inventory_columns"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    def lintables(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post-process lintables."""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []

        # If not using an EE, check for ansible-lint before we even pass off to
        # the lint action.
        if config.app == "lint" and not config.execution_environment:
            ansible_lint_location = shutil.which("ansible-lint")
            if ansible_lint_location is None:
                exit_messages.append(
                    ExitMessage(message="ansible-lint command could not be found."),
                )
                exit_messages.append(
                    ExitMessage(
                        message=(
                            "Try 'pip install ansible-lint' or consider using an execution "
                            "environment which provides ansible-lint."
                        ),
                        prefix=ExitPrefix.HINT,
                    ),
                )

        if isinstance(entry.value.current, str) and config.app == "lint":
            entry_name = entry.settings_file_path(prefix="")
            entry_source = entry.value.source
            source = abs_user_path(entry.value.current)
            try:
                mount = VolumeMount(
                    fs_source=source,
                    fs_destination=source,
                    settings_entry=entry_name,
                    source=entry_source,
                    options_string="",
                )
            except VolumeMountError as ex:
                exit_messages.append(
                    ExitMessage(
                        message=f"Error mounting lintable into execution environment: {ex}",
                    ),
                )
            else:
                self.extra_volume_mounts.append(mount)

        return messages, exit_messages

    @_post_processor
    def log_append(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process log_append"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def log_file(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process log_file

        If the parent directory for the log file cannot be created and is writable.
        If not restore to default, this will allow the writing of log messages
        even if application initialization results in a sys.exit condition
        """
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        entry.value.current = abs_user_path(entry.value.current)
        try:
            os.makedirs(os.path.dirname(entry.value.current), exist_ok=True)
            Path(entry.value.current).touch()
        except (IOError, OSError, FileNotFoundError) as exc:
            exit_msgs = [
                (
                    f"Failed to create log file {entry.value.current}"
                    f" specified in '{entry.value.source.value}'"
                ),
            ]
            exit_msgs.append(f"The error was: {str(exc)}")
            exit_messages.extend(ExitMessage(message=exit_msg) for exit_msg in exit_msgs)
            entry.value.current = entry.value.default
            entry.value.source = C.DEFAULT_CFG
            exit_msg = f"Log file set to default location: {entry.value.current}."
            exit_messages.append(ExitMessage(message=exit_msg))
            if entry.cli_parameters:
                exit_msg = (
                    f"Try again with '{entry.cli_parameters.short}"
                    " ~/ansible-navigator.log' to place it in your home directory"
                )
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
        return messages, exit_messages

    @_post_processor
    def mode(self, entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=too-many-locals
        """Post process mode

        :param entry: The current settings entry
        :param config: The full application configuration
        :raises ValueError: When more than 2 mode changes requests are present, shouldn't happen
        :returns: An instance of the standard post process return object
        """
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        subcommand_action = None
        subcommand_name = config.subcommand(config.app).name

        # Post initialization of mode processing is not needed since switching modes after
        # is not supported
        if not config.internals.initializing:
            return messages, exit_messages

        for action_package_name in config.internals.action_packages:
            try:
                action_package = importlib.import_module(action_package_name)
            except ImportError as exc:
                message = f"Unable to load action package: '{action_package_name}': {str(exc)}"
                messages.append(LogMessage(level=logging.ERROR, message=message))
                continue
            try:
                if hasattr(action_package, "get"):
                    valid_pkg_name = subcommand_name.replace("-", "_")
                    subcommand_action = action_package.get(valid_pkg_name)  # type: ignore
                break
            except (AttributeError, ModuleNotFoundError) as exc:
                message = f"Unable to load subcommand '{subcommand_name}' from"
                message += f" action package: '{action_package_name}': {str(exc)}"
                messages.append(LogMessage(level=logging.DEBUG, message=message))

        if subcommand_action is None:
            exit_msg = f"Unable to find an action for '{subcommand_name}', tried: "
            exit_msg += oxfordcomma(config.internals.action_packages, "and")
            exit_messages.append(ExitMessage(message=exit_msg))
            return messages, exit_messages

        if entry.value.current == "interactive" and os.environ.get("TERM") is None:
            exit_msg = "The TERM environment variable must be set for mode 'interactive'"
            exit_messages.append(ExitMessage(message=exit_msg))
            exit_msg = (
                "Try again after setting the TERM environment variable"
                " (e.g., 'export TERM=xterm256color') from the command line"
            )
            exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))

        # Check if the mode interactive is available for the subcommand
        # mode stdout is always available since the action base class has a `run_stdout`
        subcommand_stdout_only = not hasattr(subcommand_action, "run")
        if entry.value.current == "interactive" and subcommand_stdout_only:
            subcommand_mode_change_msgs = (
                f"Subcommand '{config.app}' does not support mode 'interactive'.",
                "Mode set to 'interactive'",
            )
            messages.extend(
                LogMessage(level=logging.INFO, message=msg) for msg in subcommand_mode_change_msgs
            )
            entry.value.current = "stdout"
            entry.value.source = C.AUTO

        # Check if any other entry has requested a mode change different than current
        mode_set = set(request.mode for request in self._requested_mode)
        if len(mode_set) == 1:
            requested = self._requested_mode[0]
            auto_mode = requested.mode.value
            if auto_mode != entry.value.current:
                entry_mode_change_msgs = (
                    f"Parameter '{requested.entry}' required mode '{auto_mode!s}'.",
                    f"Mode will be set to '{auto_mode}'",
                )
                messages.extend(
                    LogMessage(level=logging.INFO, message=msg) for msg in entry_mode_change_msgs
                )
                entry.value.current = auto_mode
                entry.value.source = C.AUTO
        elif len(mode_set) > 1:
            raise ValueError(f"Conflicting mode requests: {self._requested_mode}")
        return messages, exit_messages

    @_post_processor
    def osc4(self, entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process osc4"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def plugin_name(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process plugin_name"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if config.app == "doc" and entry.value.current is C.NOT_SET:
            if config.entry("help_doc").value.current is False:
                exit_msg = "A plugin name is required when using the doc subcommand"
                exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = "Try again with 'doc <plugin_name>'"
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                return messages, exit_messages
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def pass_environment_variable(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def playbook(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process playbook"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if config.app == "run" and entry.value.current is C.NOT_SET:
            if config.entry("help_playbook").value.current is False:
                exit_msg = "A playbook is required when using the run subcommand"
                exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = "Try again with 'run <playbook name>'"
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                return messages, exit_messages
        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @_post_processor
    def playbook_artifact_enable(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_enable"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def playbook_artifact_replay(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_replay"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if config.app == "replay" and entry.value.current is C.NOT_SET:
            exit_msg = "An playbook artifact file is required when using the replay subcommand"
            exit_messages.append(ExitMessage(message=exit_msg))
            exit_msg = "Try again with 'replay <path to playbook artifact>'"
            exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages

        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)

        if config.app == "replay":
            if not os.path.isfile(entry.value.current):
                exit_msg = (
                    f"The specified playbook artifact could not be found: {entry.value.current}"
                )
                exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = "Try again with 'replay <valid path to playbook artifact>'"
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                return messages, exit_messages
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def playbook_artifact_save_as(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process playbook_artifact_save_as"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        # literal_text, fname, format_spec, conversion
        found = set(f for _, f, _, _ in Formatter().parse(entry.value.current) if f)
        available = set(f for _, f, _, _ in Formatter().parse(entry.value.default) if f)
        unknown = found - available
        if not unknown:
            return messages, exit_messages
        exit_msg = (
            f"The playbook artifact file name '{entry.value.current}', set by"
            f" {entry.value.source.value.lower()}, has unrecognized variables:"
            f" {oxfordcomma(unknown, 'and')}"
        )
        exit_messages.append(ExitMessage(message=exit_msg))
        exit_msg = f"Try again with only {oxfordcomma(available, 'and/or')}"
        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def pull_arguments(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process ``pull_arguments``

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = to_list(entry.value.current)
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    settings_sample = partialmethod(_forced_stdout, subcommand="settings")

    @_post_processor
    def settings_schema(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Force mode stdout for schema parameter.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []

        if entry.value.source is not C.DEFAULT_CFG and config.app == "settings":
            mode = Mode.STDOUT
            self._requested_mode.append(ModeChangeRequest(entry=entry.name, mode=mode))
            message = message = f"`{entry.name} requesting mode {mode.value}"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def set_environment_variable(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process set_environment_variable"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.source in [
            C.ENVIRONMENT_VARIABLE,
            C.USER_CLI,
        ]:
            flattened = flatten_list(entry.value.current)
            set_envs = {}
            for env_var_pair in flattened:
                parts = env_var_pair.split("=")
                if len(parts) == 2:
                    set_envs[parts[0]] = parts[1]
                else:
                    exit_msg = (
                        "The following set-environment-variable"
                        f" entry could not be parsed: {env_var_pair}"
                    )
                    exit_messages.append(ExitMessage(message=exit_msg))
                    if entry.cli_parameters:
                        exit_msg = f"Try again with '{entry.cli_parameters.short} MY_VAR=my_value'"
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            entry.value.current = set_envs
        if entry.value.source is not C.NOT_SET:
            entry.value.current = {k: str(v) for k, v in entry.value.current.items()}
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def time_zone(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process ``time_zone``

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []

        exit_msg = (
            f"The specified time zone '{entry.value.current}', set by"
            f" {entry.value.source.value.lower()}, "
        )
        if isinstance(entry.value.current, str):
            available_timezones = sorted(zoneinfo.available_timezones())
            if entry.value.current in available_timezones or entry.value.current == "local":
                return messages, exit_messages
            exit_msg += "could not be found."
        else:
            exit_msg += (
                f"must be a string but was found to be a '{type(entry.value.current).__name__}'."
            )
        exit_messages.append(ExitMessage(message=exit_msg))
        exit_msg = "Please try again with a valid IANA time zone."
        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
        return messages, exit_messages
