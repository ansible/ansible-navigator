import os


from ansible_navigator.utils import flatten_list

from .definitions import Message


class PostProcess:
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
        if value.lower() in ("yes", "true", "t", "y", "1"):
            return True
        if value.lower() in ("no", "false", "f", "n", "0"):
            return False
        raise ValueError

    def _flatten_resolve_list_of_paths(self, value):
        value = flatten_list(value)
        value = [self._abs_user_path(entry) for entry in value]
        return value
    
    def execution_environment(self, entry, config):
        # pylint: disable=unused-argument
        messages = []
        errors = []
        try:
            entry.value.current = self._str2bool(entry.value.current)
        except ValueError:
            errors.append(entry.invalid_choice)
        return messages, errors


    def inventory(self, entry, config):
        messages = []
        errors = []
        inventory = entry
        if config.app == "inventory" and not inventory.value.current:
            msg = "An inventory is required when using the inventory subcommand"
            errors.append(msg)
        inventory.value.current = self._flatten_resolve_list_of_paths(inventory.value.current)
        messages.append(Message(log_level="debug", message="Completed inventory post processing"))
        return messages, errors
