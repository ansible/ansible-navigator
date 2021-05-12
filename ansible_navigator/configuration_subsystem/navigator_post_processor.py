""" post processing of ansible-navigator configuration
"""
import distutils
import importlib
import logging
import os

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
from ..utils import LogMessage


def _post_processor(func):
    def wrapper(*args, **kwargs):
        name = kwargs["entry"].name
        before = str(kwargs["entry"].value.current)
        messages, errors = func(*args, **kwargs)
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
        return messages, errors

    return wrapper


PostProcessorReturn = Tuple[List[LogMessage], List[str]]


class NavigatorPostProcessor:
    """application post processor"""

    @staticmethod
    def _true_or_false(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        messages: List[LogMessage] = []
        errors: List[str] = []
        try:
            entry.value.current = str2bool(entry.value.current)
        except ValueError:
            error = f"{entry.name} could not be converted to a boolean value,"
            error += f" value was '{entry.value.current}' ({type(entry.value.current).__name__})"
            errors.append(error)
        return messages, errors

    @staticmethod
    @_post_processor
    def collection_doc_cache_path(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process collection doc cache path"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def cmdline(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process cmdline"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if entry.value.source is C.ENVIRONMENT_VARIABLE:
            entry.value.current = entry.value.current.split()
        return messages, errors

    @_post_processor
    def editor_console(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process editor_console"""
        return self._true_or_false(entry, config)

    @_post_processor
    def execution_environment(self, entry, config) -> PostProcessorReturn:
        """Post process execution_environment"""
        messages, errors = self._true_or_false(entry, config)
        if entry.value.current is False:
            success, message = check_for_ansible()
            if success:
                messages.append(LogMessage(level=logging.DEBUG, message=message))
            else:
                errors.append(message)
        else:
            container_engine_location = distutils.spawn.find_executable(config.container_engine)
            if container_engine_location is None:
                error = "The specified container engine could not be found:"
                error += f"'{config.container_engine}',"
                error += f" set by '{config.entry('container_engine').value.source.value}'"
                errors.append(error)
        return messages, errors

    @staticmethod
    @_post_processor
    def inventory(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process inventory"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if config.app == "inventory" and entry.value.current is C.NOT_SET:
            error = "An inventory is required when using the inventory subcommand"
            errors.append(error)
            return messages, errors
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
        return messages, errors

    @staticmethod
    @_post_processor
    def inventory_column(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process inventory_columns"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, errors

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
        errors: List[str] = []
        entry.value.current = abs_user_path(entry.value.current)
        try:
            os.makedirs(os.path.dirname(entry.value.current), exist_ok=True)
            Path(entry.value.current).touch()
        except (IOError, OSError, FileNotFoundError) as exc:
            entry.value.current = entry.value.default
            entry.value.source = C.DEFAULT_CFG
            error = f"Failed to create log file {entry.value.current}"
            error += f" specified in '{entry.value.source.value}'"
            error += f" The error was: {str(exc)}"
            error += f" Log file set to default: {entry.value.current}."
            errors.append(error)
        return messages, errors

    @staticmethod
    @_post_processor
    def mode(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process mode"""
        messages: List[LogMessage] = []
        errors: List[str] = []
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
            error = f"Unable to find an action for '{subcommand_name}', tried: "
            error += oxfordcomma(config.internals.action_packages, "and")
            errors.append(error)
            return messages, errors

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
            error = f"Subcommand '{config.app}' does not support mode '{entry.value.current}'."
            error += f" Supported modes: {oxfordcomma(subcommand_modes, 'and')}."
            errors.append(error)
        return messages, errors

    @_post_processor
    def osc4(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process osc4"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def plugin_name(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process plugin_name"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if config.app == "doc" and entry.value.current is C.NOT_SET:
            error = "An plugin name is required when using the doc subcommand"
            errors.append(error)
            return messages, errors
        return messages, errors

    @staticmethod
    @_post_processor
    def pass_environment_variable(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def playbook(entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if config.app == "run" and entry.value.current is C.NOT_SET:
            error = "A playbook is required when using the run subcommand"
            errors.append(error)
            return messages, errors
        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @_post_processor
    def playbook_artifact_enable(
        self, entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_enable"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def playbook_artifact_load(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        """Post process playbook_artifact_load"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if config.app == "load" and entry.value.current is C.NOT_SET:
            error = "An playbook artifact file is required when using the load subcommand"
            errors.append(error)
            return messages, errors

        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)

        if config.app == "load":
            if not os.path.isfile(entry.value.current):
                error = f"The specified playbook artifact could not be found: {entry.value.current}"
                errors.append(error)
                return messages, errors
        return messages, errors

    @staticmethod
    @_post_processor
    def set_environment_variable(
        entry: Entry, config: ApplicationConfiguration
    ) -> PostProcessorReturn:
        # pylint: disable=unused-argument
        """Post process set_environment_variable"""
        messages: List[LogMessage] = []
        errors: List[str] = []
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
                    msg = (
                        "The following set-environment-variable"
                        f" entry could not be parsed: {env_var_pair}"
                    )
                    errors.append(msg)
            entry.value.current = set_envs
        if entry.value.source is not C.NOT_SET:
            entry.value.current = {k: str(v) for k, v in entry.value.current.items()}
        return messages, errors
