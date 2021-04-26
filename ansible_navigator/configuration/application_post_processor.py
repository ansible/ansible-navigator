import os


from .definitions import Message

from ansible_navigator.utils import Sentinel


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

    def flatten_list(self, lyst):
        if isinstance(lyst, list):
            return [a for i in lyst for a in self.flatten_list(i)]
        return [lyst]

    def _flatten_resolve_list_of_paths(self, value):
        value = self.flatten_list(value)
        value = [self._abs_user_path(entry) for entry in value]
        return value

    def _true_or_false(self, entry, config):
        # pylint: disable=unused-argument
        messages = []
        errors = []
        try:
            entry.value.current = self._str2bool(entry.value.current)
        except ValueError:
            errors.append(entry.invalid_choice)
        return messages, errors

    @_post_processor
    def editor_console(self, entry, config):
        return self._true_or_false(entry, config)

    @_post_processor
    def execution_environment(self, entry, config):
        return self._true_or_false(entry, config)

    @_post_processor
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
            entry.value.current = self._flatten_resolve_list_of_paths(entry.value.current)
        return messages, errors

    @_post_processor
    def inventory_columns(self, entry, config):
        # pylint: disable=unused-argument
        messages = []
        errors = []
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = []
        else:
            entry.value.current = self.flatten_list(entry.value.current)
            messages.append(
                Message(log_level="debug", message="Completed inventory-column post processing")
            )
        return messages, errors

    @_post_processor
    def log_file(self, entry, config):
        # pylint: disable=unused-argument
        messages = []
        errors = []
        entry.value.current = self._abs_user_path(entry.value.current)
        return messages, errors

    @_post_processor
    def osc4(self, entry, config):
        return self._true_or_false(entry, config)

    @_post_processor
    def pass_environment_variable(self, entry, config):
        # pylint: disable=unused-argument
        messages = []
        errors = []
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = []
        else:
            entry.value.current = self.flatten_list(entry.value.current)
        return messages, errors

    @_post_processor
    def set_environment_variable(self, entry, config):
        # pylint: disable=unused-argument
        messages = []
        errors = []
        if isinstance(entry.value.current, Sentinel):
            entry.value.current = {}
        elif entry.value.source.name == "USER_CLI":
            flattened = self.flatten_list(entry.value.current)
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
