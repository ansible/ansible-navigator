import os


from ansible_navigator.utils import flatten_list

from .definitions import EntrySource
from .definitions import Message

from ansible_navigator.utils import Sentinel



class ApplicationPostProcessor:
    @staticmethod
    def _abs_user_path(fpath):
        return os.path.abspath(os.path.expanduser(fpath))

    @staticmethod
    def _str2bool(value):
        """convert some commonly used values
        to a boolean
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() in ("yes", "true"):
                return True
            if value.lower() in ("no", "false"):
                return False
        raise ValueError

    def _flatten_resolve_list_of_paths(self, value):
        value = flatten_list(value)
        value = [self._abs_user_path(entry) for entry in value]
        return value
    
    def _true_or_false(self, entry, config):
        #pylint: disable=unused-argument
        messages = []
        errors = []
        try:
            entry.value.current = self._str2bool(entry.value.current)
        except ValueError:
            errors.append(entry.invalid_choice)
        return messages, errors
    
    def editor_console(self, entry, config):
        return self._true_or_false(entry, config)
    
    def execution_environment(self, entry, config):
        return self._true_or_false(entry, config)

    def inventory(self, entry, config):
        messages = []
        errors = []
        if config.app == "inventory" and not entry.value.current:
            msg = "An inventory is required when using the inventory subcommand"
            errors.append(msg)
            return messages, errors
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = []
        else:
            entry.value.current = flatten_list(entry.value.current)
            messages.append(Message(log_level="debug", message="Completed inventory post processing"))
        return messages, errors
    
    def inventory_columns(self, entry, config):
        #pylint: disable=unused-argument
        messages = []
        errors = []
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = []
        else:
            entry.value.current = flatten_list(entry.value.current)
            messages.append(Message(log_level="debug", message="Completed inventory-column post processing"))
        return messages, errors
    
    def log_file(self, entry, config):
        #pylint: disable=unused-argument
        messages = []
        errors = []
        entry.value.current = self._abs_user_path(entry.value.current)
        return messages, errors
    
    def osc4(self, entry, config):
        return self._true_or_false(entry, config)
    
    def pass_environment_variable(self, entry, config):
        #pylint: disable=unused-argument
        messages = []
        errors = []
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = []
        else:
            entry.value.current = flatten_list(entry.value.current)
        return messages, errors
    
    def set_environment_variable(self, entry, config):
        #pylint: disable=unused-argument
        messages = []
        errors = []
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = {}
        elif entry.value.source.name == EntrySource.USER_CLI:
            entry.value.current = flatten_list(entry.value.current)
            set_envs = {}
            for env_var in entry.value.current:
                parts = env_var.split("=")
                if len(parts) == 2:
                    set_envs[parts[0]] = parts[1]
                else:
                    msg = (
                        "The following set-environment-variable"
                        f" entry could not be parsed: {env_var}"
                    )
                    errors.append(msg)
            entry.value.current = set_envs
        return messages, errors