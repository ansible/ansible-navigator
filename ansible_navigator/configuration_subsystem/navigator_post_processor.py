""" post processing of ansible-navigator configuration
"""
import importlib
import logging
import os
import shlex
import shutil

from pathlib import Path
from typing import List
from typing import Tuple

from .definitions import Constants as C
from .definitions import Entry
from .definitions import ApplicationConfiguration

from ..utils import abs_user_path
from ..utils import check_for_ansible
from ..utils import flatten_list
from ..utils import oxfordcomma
from ..utils import str2bool
from ..utils import to_list
from ..utils import LogMessage
from ..utils import ExitMessage
from ..utils import ExitPrefix


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
            )
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

    @staticmethod
    def _true_or_false(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
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
    def collection_doc_cache_path(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process collection doc cache path"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def cmdline(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process cmdline"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if isinstance(entry.value.current, str):
            entry.value.current = shlex.split(entry.value.current)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def container_engine(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process container_engine"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current == "auto":
            choices = filter(lambda x: x != "auto", entry.choices)
            for choice in choices:
                if shutil.which(choice):
                    entry.value.current = choice
                    break
        return messages, exit_messages

    @_post_processor
    def display_color(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process displacy_color"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.source == C.ENVIRONMENT_VARIABLE:
            entry.value.current = False
            message = f"{entry.environment_variable()} was set, set to {entry.value.current}"
            messages.append(LogMessage(level=logging.INFO, message=message))
            return messages, exit_messages
        return self._true_or_false(entry, config)

    @_post_processor
    def editor_console(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process editor_console"""
        return self._true_or_false(entry, config)

    @_post_processor
    def execution_environment(self, entry, config) -> PostProcessorReturn:
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
                entry_short = entry.cli_parameters.short
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
        else:
            new_messages, new_exit_messages = check_for_ansible()
            messages.extend(new_messages)
            exit_messages.extend(new_exit_messages)
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def execution_environment_image(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process execution_environment_image"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if ":" not in entry.value.current:
            entry.value.current = f"{entry.value.current}:latest"
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def execution_environment_volume_mounts(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process set_environment_variable"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.source in [
            C.ENVIRONMENT_VARIABLE,
            C.USER_CLI,
        ]:
            volume_mounts = flatten_list(entry.value.current)
            for mount_path in volume_mounts:
                parts = mount_path.split(":")
                if len(parts) > 3:
                    exit_msg = (
                        "The following execution-environment-volume-mounts"
                        f" entry could not be parsed: {mount_path}"
                    )
                    exit_messages.append(ExitMessage(message=exit_msg))
                    if entry.cli_parameters:
                        exit_msg = (
                            "Try again with format "
                            + f"'{entry.cli_parameters.short}"
                            + " <source-path>:<destination-path>:<label(Z or z)>'."
                            + " Note: label is optional."
                        )
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                    return messages, exit_messages

            entry.value.current = volume_mounts

        elif entry.value.current is not C.NOT_SET:
            parsed_volume_mounts = []
            volume_mounts = to_list(entry.value.current)
            for mount_obj in volume_mounts:
                if not isinstance(mount_obj, dict):
                    exit_msg = (
                        "The following execution-environment.volume-mounts"
                        f" entry could not be parsed: {mount_obj}"
                    )
                    exit_messages.append(ExitMessage(message=exit_msg))
                    if entry.cli_parameters:
                        exit_msg = (
                            "The value of execution-environment.volume-mounts"
                            + "should be list of dictionaries"
                            + " and valid keys are 'src', 'dest' and 'label'."
                        )
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                    return messages, exit_messages

                try:
                    mount_path = f"{mount_obj['src']}:{mount_obj['dest']}"
                    if mount_obj.get("label"):
                        mount_path += f":{mount_obj['label']}"
                    parsed_volume_mounts.append(mount_path)
                except KeyError as exc:
                    exit_msg = (
                        f"Failed to parse following execution-environment.volume-mounts"
                        f" entry: '{mount_obj}'. Value of '{str(exc)}' key not provided."
                    )
                    exit_messages.append(ExitMessage(message=exit_msg))
                    exit_hint_msg = (
                        " Valid keys are 'src', 'dest' and 'label'. Note: label key is optional."
                    )
                    exit_messages.append(ExitMessage(message=exit_hint_msg, prefix=ExitPrefix.HINT))

                    return messages, exit_messages

            entry.value.current = parsed_volume_mounts
        return messages, exit_messages

    @_post_processor
    def help_config(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process help_config"""
        messages, exit_messages = self._true_or_false(entry, config)
        if all((entry.value.current is True, config.app == "config", config.mode == "interactive")):
            if entry.cli_parameters:
                long_hc = entry.cli_parameters.long_override or entry.name_dashed
                exit_msg = (
                    f"{entry.cli_parameters.short} or --{long_hc}"
                    " is valid only when 'mode' argument is set to 'stdout'"
                )
                exit_messages.append(ExitMessage(message=exit_msg))
                mode_cli = config.entry("mode").cli_parameters
                if mode_cli:
                    m_short = mode_cli.short
                    if m_short:
                        exit_msg = f"Try again with '{m_short} stdout'"
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                return messages, exit_messages
        return messages, exit_messages

    @_post_processor
    def help_doc(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process help_doc"""
        messages, exit_messages = self._true_or_false(entry, config)
        if all((entry.value.current is True, config.app == "doc", config.mode == "interactive")):
            if entry.cli_parameters:
                long_hd = entry.cli_parameters.long_override or entry.name_dashed
                exit_msg = (
                    f"{entry.cli_parameters.short} or --{long_hd}"
                    " is valid only when 'mode' argument is set to 'stdout'"
                )
                exit_messages.append(ExitMessage(message=exit_msg))
                mode_cli = config.entry("mode").cli_parameters
                if mode_cli:
                    m_short = mode_cli.short
                    if m_short:
                        exit_msg = f"Try again with '{m_short} stdout'"
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages
        return messages, exit_messages

    @_post_processor
    def help_inventory(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process help_inventory"""
        messages, exit_messages = self._true_or_false(entry, config)
        if all(
            (entry.value.current is True, config.app == "inventory", config.mode == "interactive")
        ):
            if entry.cli_parameters:
                long_hd = entry.cli_parameters.long_override or entry.name_dashed
                exit_msg = (
                    f"{entry.cli_parameters.short} or --{long_hd}"
                    " is valid only when 'mode' argument is set to 'stdout'"
                )
                exit_messages.append(ExitMessage(message=exit_msg))
                mode_cli = config.entry("mode").cli_parameters
                if mode_cli:
                    m_short = mode_cli.short
                    if m_short:
                        exit_msg = f"Try again with '{m_short} stdout'"
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages
        return messages, exit_messages

    @_post_processor
    def help_playbook(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process help_playbook"""
        messages, exit_messages = self._true_or_false(entry, config)
        if all((entry.value.current is True, config.app == "run", config.mode == "interactive")):
            if entry.cli_parameters:
                long_hp = entry.cli_parameters.long_override or entry.name_dashed
                exit_msg = (
                    f"{entry.cli_parameters.short} or --{long_hp}"
                    " is valid only when 'mode' argument is set to 'stdout'"
                )
                exit_messages.append(ExitMessage(message=exit_msg))
                mode_cli = config.entry("mode").cli_parameters
                if mode_cli:
                    m_short = mode_cli.short
                    if m_short:
                        exit_msg = f"Try again with '{m_short} stdout'"
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def inventory(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process inventory"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if config.app == "inventory" and entry.value.current is C.NOT_SET:
            if not (
                config.entry("help_inventory").value.current
                and config.entry("mode").value.current == "stdout"
            ):
                exit_msg = "An inventory is required when using the inventory subcommand"
                exit_messages.append(ExitMessage(message=exit_msg))
                if entry.cli_parameters:
                    exit_msg = f"Try again with '{entry.cli_parameters.short} <path to inventory>'"
                    exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
                return messages, exit_messages
        if entry.value.current is not C.NOT_SET:
            flattened = flatten_list(entry.value.current)
            entry.value.current = []
            for inv_entry in flattened:
                if "," in inv_entry:
                    # host list
                    entry.value.current.append(inv_entry)
                else:
                    # file path
                    entry.value.current.append(abs_user_path(inv_entry))
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def inventory_column(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process inventory_columns"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, exit_messages

    @_post_processor
    def log_append(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process log_append"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def log_file(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process log_file

        If the parent directory for the log file cannot be created adn is writable.
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
                )
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

    @staticmethod
    @_post_processor
    def mode(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=too-many-statements
        """Post process mode"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        subcommand_action = None
        subcommand_name = config.subcommand(config.app).name

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

        subcommand_modes = []

        try:
            getattr(subcommand_action, "run_stdout")
        except AttributeError:
            pass
        else:
            subcommand_modes.append("stdout")

        try:
            getattr(subcommand_action, "run")
        except AttributeError:
            pass
        else:
            subcommand_modes.append("interactive")

        if entry.value.current not in subcommand_modes:
            exit_msg = f"Subcommand '{config.app}' does not support mode '{entry.value.current}'."
            exit_msg += f" Supported modes: {oxfordcomma(subcommand_modes, 'and')}."
            exit_messages.append(ExitMessage(message=exit_msg))
            mode_cli = config.entry("mode").cli_parameters
            if mode_cli:
                other = [
                    f"{mode_cli.short} {mode}"
                    for mode in subcommand_modes
                    if mode != entry.value.current
                ]
                exit_msg = f"Try again with {oxfordcomma(other, 'or')}"
                exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
        return messages, exit_messages

    @_post_processor
    def osc4(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process osc4"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def plugin_name(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process plugin_name"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if all(
            (
                config.app == "doc",
                entry.value.current is C.NOT_SET,
                config.help_doc is False,
                config.mode != "stdout",
            )
        ):
            exit_msg = "A plugin name is required when using the doc subcommand"
            exit_messages.append(ExitMessage(message=exit_msg))
            exit_msg = "Try again with 'doc <plugin_name>'"
            exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            return messages, exit_messages
        return messages, exit_messages

    @staticmethod
    @_post_processor
    def pass_environment_variable(
        entry: Entry, config: ApplicationConfiguration
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
    def playbook(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[LogMessage] = []
        exit_messages: List[ExitMessage] = []
        if config.app == "run" and entry.value.current is C.NOT_SET:
            if not (
                config.entry("help_playbook").value.current
                and config.entry("mode").value.current == "stdout"
            ):
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
        self, entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_enable"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def playbook_artifact_replay(
        entry: Entry, config: ApplicationConfiguration
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
    def set_environment_variable(
        entry: Entry, config: ApplicationConfiguration
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
                        exit_msg = f"Try again with '{entry.cli_parameters.short} MYVAR=myvalue'"
                        exit_messages.append(ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT))
            entry.value.current = set_envs
        if entry.value.source is not C.NOT_SET:
            entry.value.current = {k: str(v) for k, v in entry.value.current.items()}
        return messages, exit_messages
