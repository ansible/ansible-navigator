""" post processing of ansible-navigator configuration
"""
import logging

from distutils.spawn import find_executable

from typing import List
from typing import Tuple

from .definitions import Constants as C
from .definitions import Entry
from .definitions import ApplicationConfiguration

from ..initialization import check_for_ansible

from ..utils import abs_user_path
from ..utils import flatten_list
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
            errors.append(entry.invalid_choice)
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
        if errors:
            return messages, errors
        if entry.value.current is False:
            success, msg = check_for_ansible()
            if success:
                messages.append(("debug", msg))
            else:
                errors.append(msg)
        else:
            container_engine_location = find_executable(config.container_engine)
            if container_engine_location is None:
                error = f"The specified container engine could not be found: '{config.container_engine}',"
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
        """Post process log_file"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @_post_processor
    def osc4(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process osc4"""
        return self._true_or_false(entry, config)

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
        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)
        return messages, errors
    
    @_post_processor
    def playbook_artifact_enable(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process playbook_artifact_enable"""
        return self._true_or_false(entry, config)
    
    @_post_processor
    def playbook_artifact_load(self, entry: Entry, config: ApplicationConfiguration) -> PostProcessorReturn:
        """Post process playbook_artifact_load"""
        messages: List[LogMessage] = []
        errors: List[str] = []
        if config.app == "load" and entry.value.current is C.NOT_SET:
            error = "An playbook artifact file is required when using the load subcommand"
            errors.append(error)
            return messages, errors
        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)
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
