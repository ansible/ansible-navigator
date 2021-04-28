""" post processing of ansible-navigator configuration
"""
from typing import List
from typing import Tuple

from .definitions import Entry
from .definitions import EntrySource
from .definitions import Config
from .definitions import Message

from ..utils import abs_user_path
from ..utils import flatten_list
from ..utils import str2bool
from ..utils import Sentinel


def _post_processor(func):
    def wrapper(*args, **kwargs):
        name = kwargs["entry"].name
        before = str(kwargs["entry"].value.current)
        messages, errors = func(*args, **kwargs)
        after = str(kwargs["entry"].value.current)
        msg = f"Completed post processing for {name} before: '{before}' after: '{after}'"
        messages.append(("debug", msg))
        return messages, errors

    return wrapper


class ApplicationPostProcessor:
    """application post processor"""

    @staticmethod
    def _true_or_false(entry: Entry, config: Config) -> Tuple[List[Message], List[str]]:
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
    def cmdline(entry: Entry, config: Config) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process cmdline"""
        messages: List[Message] = []
        errors: List[str] = []
        if isinstance(entry.value.source, EntrySource):
            if entry.value.source.name == "ENVIRONMENT_VARIABLE":
                entry.value.current = entry.value.current.split()
        return messages, errors

    @_post_processor
    def editor_console(self, entry, config) -> Tuple[List[Message], List[str]]:
        """Post process editor_console"""
        return self._true_or_false(entry, config)

    @_post_processor
    def execution_environment(self, entry, config) -> Tuple[List[Message], List[str]]:
        """Post process execution_environment"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def inventory(entry, config) -> Tuple[List[Message], List[str]]:
        """Post process inventory"""
        messages: List[Message] = []
        errors: List[str] = []
        if config.app == "inventory" and entry.value.current is Sentinel:
            msg = "An inventory is required when using the inventory subcommand"
            errors.append(msg)
            return messages, errors
        if entry.value.current is Sentinel:
            entry.value.current = []
        else:
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
    def inventory_column(entry, config) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process inventory_columns"""
        messages: List[Message] = []
        errors: List[str] = []
        if entry.value.current is Sentinel:
            entry.value.current = []
        else:
            entry.value.current = flatten_list(entry.value.current)
            messages.append(
                Message(log_level="debug", message="Completed inventory-column post processing")
            )
        return messages, errors

    @staticmethod
    @_post_processor
    def log_file(entry, config) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process log_file"""
        messages: List[Message] = []
        errors: List[str] = []
        entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @_post_processor
    def osc4(self, entry, config) -> Tuple[List[Message], List[str]]:
        """Post process osc4"""
        return self._true_or_false(entry, config)

    @staticmethod
    @_post_processor
    def pass_environment_variable(entry, config) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[Message] = []
        errors: List[str] = []
        if entry.value.current is Sentinel:
            entry.value.current = []
        else:
            entry.value.current = flatten_list(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def playbook(entry, config) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process pass_environment_variable"""
        messages: List[Message] = []
        errors: List[str] = []
        if isinstance(entry.value.current, str):
            entry.value.current = abs_user_path(entry.value.current)
        return messages, errors

    @staticmethod
    @_post_processor
    def set_environment_variable(entry, config) -> Tuple[List[Message], List[str]]:
        # pylint: disable=unused-argument
        """Post process set_environment_variable"""
        messages: List[Message] = []
        errors: List[str] = []
        if entry.value.current is Sentinel:
            entry.value.current = {}
        elif entry.value.source.name in ["ENVIRONMENT_VARIABLE", "USER_CLI"]:
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
