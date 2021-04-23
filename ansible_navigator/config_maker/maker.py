import json

from ansible_navigator.yaml import SafeLoader
from ansible_navigator.yaml import yaml


from ansible_navigator.utils import error_and_exit_early

from .parser import Parser
from .definitions import EntrySource
from .definitions import Message

from .ansible_navigator_config import CONFIG


class ConfigurationMaker:
    def __init__(self, params, settings_file_path, config=CONFIG):
        self._config = config
        self._errors = []
        self._messages = []
        self._params = params
        self._settings_file_path = settings_file_path

    def run(self):
        self.set_defaults()
        self.set_from_params()

        self.set_from_settings_file()
        if self._errors:
            error_and_exit_early(errors=self._errors)

        self.post_process()
        if self._errors:
            error_and_exit_early(errors=self._errors)
        return self._messages, self._config

    def set_defaults(self):
        for entry in self._config.entries:
            entry.value.current = entry.value.default
            entry.value.source = EntrySource.DEFAULT_CFG

    def set_from_params(self):
        parser = Parser(self._config).parser
        args, cmdline = parser.parse_known_args(self._params)
        self._config.entry("cmdline").value.current = cmdline
        for param, value in vars(args).items():
            self._config.entry(param).value.current = value
            self._config.entry(param).value.source = EntrySource.USER_CLI

    def set_from_settings_file(self):
        with open(self._settings_file_path, "r") as config_fh:
            try:
                config = yaml.load(config_fh, Loader=SafeLoader)
            except yaml.ScannerError:
                msg = f"Config file at {self._settings_file_path} but failed to parse it."
                self._errors.append(msg)
                return
        for entry in self._config.entries:
            if not entry.internal:
                path_str = entry.settings_file_path or entry.cli_parameters.long.replace("--", "")
                path_parts = [self._config.root_settings_key] + path_str.split(".")
                data = config
                try:
                    for chunk in path_parts:
                        data = data[chunk]
                    entry.value.current = data
                    entry.value.source = EntrySource.USER_CLI
                except KeyError:
                    msg = f"{path_str} not found in settings file"
                    self._messages.append(Message(log_level="debug", message=msg))

    def post_process(self):
        for entry in self._config.entries:
            if entry.post_process:
                messages, errors = entry.post_process(entry, self._config)
                self._messages.extend(messages)
                self._errors.extend(errors)
