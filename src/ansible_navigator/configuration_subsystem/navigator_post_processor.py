# pylint: disable=too-many-lines
"""Post processing of ansible-navigator configuration."""
from __future__ import annotations

import contextlib
import importlib
import logging
import os
import shlex
import shutil
import subprocess
import sys
import zoneinfo

from functools import partialmethod
from itertools import chain
from itertools import repeat
from pathlib import Path
from string import Formatter

from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.definitions import ExitPrefix
from ansible_navigator.utils.definitions import LogMessage
from ansible_navigator.utils.functions import abs_user_path
from ansible_navigator.utils.functions import check_for_ansible
from ansible_navigator.utils.functions import check_playbook_type
from ansible_navigator.utils.functions import flatten_list
from ansible_navigator.utils.functions import oxfordcomma
from ansible_navigator.utils.functions import str2bool
from ansible_navigator.utils.functions import to_list

from .definitions import ApplicationConfiguration
from .definitions import CliParameters
from .definitions import Constants as C
from .definitions import Mode
from .definitions import ModeChangeRequest
from .definitions import PaeChangeRequest
from .definitions import SettingsEntry
from .definitions import VolumeMount
from .definitions import VolumeMountError


def _post_processor(func):
    """Decorate a post processing function.

    :param func: The function to wrap
    :returns: The wrapped function
    """

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


PostProcessorReturn = tuple[list[LogMessage], list[ExitMessage]]


class NavigatorPostProcessor:
    # pylint:disable=too-many-public-methods
    """Application post processor."""

    def __init__(self):
        """Initialize the post processor."""
        #: Volume mounts accumulated from post processing various config entries.
        #: These get processed towards the end, in the (delayed)
        #: :meth:`.execution_environment_volume_mounts` post-processor.
        self.extra_volume_mounts: list[VolumeMount] = []
        self._requested_mode: list[ModeChangeRequest] = []
        self._requested_pae: list[PaeChangeRequest] = []

    @staticmethod
    def _true_or_false(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process a boolean value.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        with contextlib.suppress(ValueError):
            entry.value.current = str2bool(entry.value.current)

        return messages, exit_messages

    @staticmethod
    @_post_processor
    def ansible_runner_artifact_dir(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process ansible_runner_artifact_dir path.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def ansible_runner_rotate_artifacts_count(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process ansible_runner_rotate_artifacts_count.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            try:
                entry.value.current = int(entry.value.current)
            except ValueError as exc:
                exit_msg = f"Value should be valid integer. Failed with error {exc!s}"
                exit_messages.append(ExitMessage(message=exit_msg))
        return messages, exit_messages

    # Post process ansible_runner_write_job_events.
    ansible_runner_write_job_events = _true_or_false

    @staticmethod
    @_post_processor
    def ansible_runner_timeout(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process ansible_runner_timeout.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            try:
                entry.value.current = int(entry.value.current)
            except ValueError as exc:
                exit_msg = f"Value should be valid integer. Failed with error {exc!s}"
                exit_messages.append(ExitMessage(message=exit_msg))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def collection_doc_cache_path(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process collection doc cache path.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def cmdline(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process cmdline.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if isinstance(entry.value.current, str):
            entry.value.current = shlex.split(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def container_engine(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process container_engine.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
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
        """Post process display_color.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = False
            message = f"{entry.environment_variable()} was set, set to {entry.value.current}"
            messages.append(LogMessage(level=logging.INFO, message=message))
            return messages, exit_messages
        return self._true_or_false(entry, config)

    # Post process editor_console.
    editor_console = _true_or_false

    @_post_processor
    def execution_environment(self, entry: SettingsEntry, config) -> PostProcessorReturn:
        # pylint: disable=too-many-locals
        """Post process execution_environment.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
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
            # except on Darwin (macOS)
            message_queue_path = "/dev/mqueue/"
            mqueue_is_not_dir = not Path(message_queue_path).is_dir()
            os_is_not_mac = sys.platform != "darwin"
            ce_is_podman = config.container_engine == "podman"
            if all((ce_is_podman, mqueue_is_not_dir, os_is_not_mac)):
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
        """Post process execution_environment_image.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
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
        # pylint: disable=too-many-locals

        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        entry_name = entry.settings_file_path(prefix="")
        entry_source = entry.value.source
        volume_mounts: list[VolumeMount] = []

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
                        f" {mount_str} ({entry.value.source.value}). Errors were found: {exc!s}"
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
                            f" ({entry_source.value}). Errors were found: {exc!s}"
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
        """Post process container_options.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = to_list(entry.value.current)
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    @_post_processor
    def _disable_pae_and_enforce_stdout(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Disable playbook artifact creation and force mode stdout for a settings parameter.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages, exit_messages = self._true_or_false(entry, config)
        if entry.value.current is True:
            mode = Mode.STDOUT
            playbook_artifact_enable = False
            self._requested_mode.append(ModeChangeRequest(entry=entry.name, mode=mode))
            self._requested_pae.append(
                PaeChangeRequest(
                    entry=entry.name, playbook_artifact_enable=playbook_artifact_enable
                )
            )
            message = (
                f"`{entry.name} requesting mode {mode.value} and pae as {playbook_artifact_enable}"
            )
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        return messages, exit_messages

    # Post process for enable_prompts
    enable_prompts = _disable_pae_and_enforce_stdout

    # Post process for exec_shell
    exec_shell = _true_or_false

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
            message = f"`{entry.name} requesting mode {mode.value}"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        return messages, exit_messages

    help_builder = partialmethod(_forced_stdout, subcommand="builder")
    help_config = partialmethod(_forced_stdout, subcommand="config")
    help_doc = partialmethod(_forced_stdout, subcommand="doc")
    help_inventory = partialmethod(_forced_stdout, subcommand="inventory")

    # Post process for help_playbook
    help_playbook = _disable_pae_and_enforce_stdout

    @_post_processor
    def images_details(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process execution_environment_image_details.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

        entry.value.current = flatten_list(entry.value.current)
        # In the case --default was provided, set it to everything
        if not entry.value.current:
            entry.value.current = entry.value.default

        # Only force mode stdout if from the CLI so the values can be kept in settings
        # or in an environment variable and used with only --mode stdout
        if entry.value.source is C.USER_CLI:
            mode = Mode.STDOUT
            self._requested_mode.append(ModeChangeRequest(entry=entry.name, mode=mode))
            message = f"`{entry.name} requesting mode {mode.value}"
            messages.append(LogMessage(level=logging.DEBUG, message=message))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def inventory(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process inventory.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

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
        """Post process inventory_columns.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    def lintables(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post-process lintables.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

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
            else:
                try:
                    subprocess.run("ansible-lint --version", shell=True, check=True)
                except subprocess.CalledProcessError:
                    exit_messages.append(
                        ExitMessage(
                            message=("ansible-lint does not seem to be installed correctly.")
                        ),
                    )
                    exit_messages.append(
                        ExitMessage(
                            message=(
                                "Ensure the command `ansible-lint --version` can be run prior to"
                                " using ansible-navigator"
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

    # Post process log_append.
    log_append = _true_or_false

    @staticmethod
    @_post_processor
    def log_file(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process log_file.

        If the parent directory for the log file cannot be created and is writable.
        If not restore to default, this will allow the writing of log messages
        even if application initialization results in a sys.exit condition

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        entry.value.current = abs_user_path(entry.value.current)
        try:
            os.makedirs(os.path.dirname(entry.value.current), exist_ok=True)
            Path(entry.value.current).touch()
        except (OSError, FileNotFoundError) as exc:
            exit_msgs = [
                (
                    f"Failed to create log file {entry.value.current}"
                    f" specified in '{entry.value.source.value}'"
                ),
            ]
            exit_msgs.append(f"The error was: {exc!s}")
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
        """Post process mode.

        :param entry: The current settings entry
        :param config: The full application configuration
        :raises ValueError: When more than 2 mode changes requests are present, shouldn't happen
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
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
                message = f"Unable to load action package: '{action_package_name}': {exc!s}"
                messages.append(LogMessage(level=logging.ERROR, message=message))
                continue
            try:
                if hasattr(action_package, "get"):
                    valid_pkg_name = subcommand_name.replace("-", "_")
                    subcommand_action = action_package.get(valid_pkg_name)  # type: ignore
                break
            except (AttributeError, ModuleNotFoundError) as exc:
                message = f"Unable to load subcommand '{subcommand_name}' from"
                message += f" action package: '{action_package_name}': {exc!s}"
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
        mode_set = {request.mode for request in self._requested_mode}
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
            msg = f"Conflicting mode requests: {self._requested_mode}"
            raise ValueError(msg)
        return messages, exit_messages

    # Post process osc4.
    osc4 = _true_or_false

    @_post_processor
    def plugin_name(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process plugin_name.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

        is_not_subcommand_match = config.entry("app").value.current != "doc"
        if is_not_subcommand_match:
            # Subcommand is different
            return messages, exit_messages

        is_help = config.entry("help_doc").value.current is True
        if is_help:
            # Help is requested
            return messages, exit_messages

        # Determine if mode stdout should be set
        if config.initial is None:
            force_stdout_for = {
                "-l",  # List plugins
                "--list",  # List plugins
                "-F",  # List plugin files
                "--list_files",  # List plugin files
                "-s",  # Print a snippet
                "--snippet",  # Print a snippet
                "--metadata-dump",  # Print a metadata dump
            }
            cmdline = config.entry("cmdline").value.current
            if isinstance(cmdline, list) and force_stdout_for.intersection(cmdline):
                mode = Mode.STDOUT
                self._requested_mode.append(ModeChangeRequest(entry=entry.name, mode=mode))
                message = message = f"`{entry.name} requesting mode {mode.value}"
                messages.append(LogMessage(level=logging.DEBUG, message=message))
                return messages, exit_messages

        is_not_set = entry.value.current is C.NOT_SET
        if is_not_set:
            # A plugin name is required
            exit_msg = "A plugin name or other parameter is required when using the doc subcommand"
            exit_messages.append(ExitMessage(message=exit_msg))
            exit_msg = "Try again with 'doc <plugin_name>'"
            exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def pass_environment_variable(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process pass_environment_variable.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def playbook(entry: SettingsEntry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process playbook.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if (
            config.app == "run"
            and entry.value.current is C.NOT_SET
            and config.entry("help_playbook").value.current is False
        ):
            exit_msg = "A playbook is required when using the run subcommand"
            exit_messages.append(ExitMessage(message=exit_msg))
            exit_msg = "Try again with 'run <playbook name>'"
            exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages
        if check_playbook_type(entry.value.current) == "file" and isinstance(
            entry.value.current, str
        ):
            entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @_post_processor
    def playbook_artifact_enable(
        self,
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_enable.

        :param entry: The current settings entry
        :param config: The full application configuration
        :raises ValueError: When more than 1 pae changes requests are present, shouldn't happen
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

        # Check if any other entry has requested a pae change different than current
        pae_set = {request.playbook_artifact_enable for request in self._requested_pae}
        if len(pae_set) == 1:
            requested = self._requested_pae[0]
            auto_pae = requested.playbook_artifact_enable
            if auto_pae != entry.value.current:
                pae_change_msgs = (
                    f"Parameter '{requested.entry}' required pae '{auto_pae!s}'.",
                    f"Pae will be set to '{auto_pae}'",
                )
                messages.extend(
                    LogMessage(level=logging.INFO, message=msg) for msg in pae_change_msgs
                )
                entry.value.current = auto_pae
        elif len(pae_set) > 1:
            msg = f"Conflicting pae requests: {self._requested_pae}"
            raise ValueError(msg)
        with contextlib.suppress(ValueError):
            entry.value.current = str2bool(entry.value.current)

        return messages, exit_messages

    @staticmethod
    @_post_processor
    def playbook_artifact_replay(
        entry: SettingsEntry,
        config: ApplicationConfiguration,
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_replay.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if config.app == "replay" and entry.value.current is C.NOT_SET:
            exit_msg = "An playbook artifact file is required when using the replay subcommand"
            exit_messages.append(ExitMessage(message=exit_msg))
            exit_msg = "Try again with 'replay <path to playbook artifact>'"
            exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages

        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)

        if config.app == "replay" and not os.path.isfile(entry.value.current):
            exit_msg = f"The specified playbook artifact could not be found: {entry.value.current}"
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
        """Post process playbook_artifact_save_as.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        # literal_text, fname, format_spec, conversion
        found = {f for _, f, _, _ in Formatter().parse(entry.value.current) if f}
        available = {f for _, f, _, _ in Formatter().parse(entry.value.default) if f}
        non_defaults_also_available = {"playbook_status"}

        available.update(non_defaults_also_available)
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
        """Post process ``pull_arguments``.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = to_list(entry.value.current)
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    settings_effective = partialmethod(_forced_stdout, subcommand="settings")
    settings_sample = partialmethod(_forced_stdout, subcommand="settings")
    settings_sources = partialmethod(_forced_stdout, subcommand="settings")

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
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

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
        """Post process set_environment_variable.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []
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
        """Post process ``time_zone``.

        :param entry: The current settings entry
        :param config: The full application configuration
        :returns: An instance of the standard post process return object
        """
        messages: list[LogMessage] = []
        exit_messages: list[ExitMessage] = []

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
