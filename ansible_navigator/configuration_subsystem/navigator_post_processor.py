""" post processing of ansible-navigator configuration
"""
from typing import List
from typing import Tuple

from .definitions import Constants as C
from .definitions import Entry
from .definitions import ApplicationConfiguration
from .definitions import Message

from ..utils import abs_user_path
from ..utils import flatten_list
from ..utils import str2bool


def _post_processor(func):
    def wrapper(*args, **kwargs):
        name = kwargs["entry"].name
        before = str(kwargs["entry"].value.current)
        messages, errors = func(*args, **kwargs)
        after = str(kwargs["entry"].value.current)
        changed = before != after
        messages.append(("debug", f"Completed post processing for {name}. (changed={changed})"))
        if changed:
            messages.append(("debug", f" before: '{before}'"))
            messages.append(("debug", f" after: '{after}'"))
        return messages, errors

    return wrapper


class NavigatorPostProcessor:
    """application post processor"""

    @staticmethod
    def _true_or_false(
        entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        messages: List[Message] = []
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
    ) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process collection doc cache path"""
        messages: List[Message] = []
        errors: List[str] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def cmdline(entry: Entry, config: ApplicationConfiguration) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process cmdline"""
        messages: List[Message] = []
        errors: List[str] = []
        if entry.value.source is C.ENVIRONMENT_VARIABLE:
            entry.value.current = entry.value.current.split()
        return messages, errors

    @_post_processor
    def editor_console(
        self, entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        """Post process editor_console"""
        return self._true_or_false(entry, config)

    @_post_processor
    def execution_environment(self, entry, config) -> Tuple[List[Message], List[str]]:
        """Post process execution_environment"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def inventory(
        entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        """Post process inventory"""
        messages: List[Message] = []
        errors: List[str] = []
        if config.app == "inventory" and entry.value.current is C.NOT_SET:
            msg = "An inventory is required when using the inventory subcommand"
            errors.append(msg)
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
    def inventory_column(
        entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process inventory_columns"""
        messages: List[Message] = []
        errors: List[str] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def log_file(entry: Entry, config: ApplicationConfiguration) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process log_file"""
        messages: List[Message] = []
        errors: List[str] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @_post_processor
    def osc4(
        self, entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        """Post process osc4"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def pass_environment_variable(
        entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[Message] = []
        errors: List[str] = []
        if entry.value.current is not C.NOT_SET:
            entry.value.current = flatten_list(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def playbook(entry: Entry, config: ApplicationConfiguration) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[Message] = []
        errors: List[str] = []
        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def set_environment_variable(
        entry: Entry, config: ApplicationConfiguration
    ) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process set_environment_variable"""
        messages: List[Message] = []
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
        return messages, errors
