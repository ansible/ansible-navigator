import os

from ansible_navigator.yaml import SafeLoader
from ansible_navigator.yaml import yaml


from ansible_navigator.utils import error_and_exit_early

from .parser import Parser
from .definitions import EntrySource
from .definitions import Message

from .ansible_navigator_config import CONFIG


class ConfigurationMaker:
    def __init__(self, params, settings_file_path, apply_original_cli = False, config=CONFIG, save_as_intitial = False):
        self._apply_roginal_cli = apply_original_cli
        self._config = config
        self._errors = []
        self._messages = []
        self._params = params
        self._save_as_init = save_as_intitial
        self._settings_file_path = settings_file_path

    def run(self):
        self._set_defaults()
        self._set_from_settings_file()
        self._set_from_environment_variable()
        self._set_from_params()
        if self._errors:
            error_and_exit_early(errors=self._errors)

        self._post_process()
        if self._errors:
            error_and_exit_early(errors=self._errors)

        self._check_choices()
        if self._errors:
            error_and_exit_early(errors=self._errors)

        return self._messages, self._config

    def _set_defaults(self):
        for entry in self._config.entries:
            entry.value.current = entry.value.default
            entry.value.source = EntrySource.DEFAULT_CFG

    def _set_from_settings_file(self):
        with open(self._settings_file_path, "r") as config_fh:
            try:
                config = yaml.load(config_fh, Loader=SafeLoader)
            except yaml.ScannerError:
                msg = f"Settings file found {self._settings_file_path}, but failed to load it."
                self._errors.append(msg)
                return
        for entry in self._config.entries:
            if not entry.internal:
                settings_file_path = entry.settings_file_path(self._config.application_name)
                path_parts = settings_file_path.split(".")
                data = config
                try:
                    for chunk in path_parts:
                        data = data[chunk]
                    entry.value.current = data
                    entry.value.source = EntrySource.USER_CFG
                except KeyError:
                    msg = f"{settings_file_path} not found in settings file"
                    self._messages.append(Message(log_level="debug", message=msg))

    def _set_from_environment_variable(self):
        for entry in self._config.entries:
            if not entry.internal:
                set_envvar = os.environ.get(entry.environment_variable(self._config.application_name))
                if set_envvar is not None:
                    entry.value.current = set_envvar
                    entry.value.source = EntrySource.ENVIRONMENT_VARIABLE

    def _set_from_params(self):
        parser = Parser(self._config).parser
        args, cmdline = parser.parse_known_args(self._params)
        self._config.entry("cmdline").value.current = cmdline
        for param, value in vars(args).items():
            self._config.entry(param).value.current = value
            self._config.entry(param).value.source = EntrySource.USER_CLI

    def _post_process(self):
        for entry in self._config.entries:
            if entry.post_process:
                messages, errors = entry.post_process(entry, self._config)
                self._messages.extend(messages)
                self._errors.extend(errors)
    
    def _check_choices(self):
        for entry in self._config.entries:
            if not entry.internal and entry.choices:
                if entry.value.current not in entry.choices:
                    self._errors.append(entry.invalid_choice)


