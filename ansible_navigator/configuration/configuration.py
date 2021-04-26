import json
import os
import pickle

from copy import deepcopy

from ansible_navigator.yaml import SafeLoader
from ansible_navigator.yaml import yaml


from ansible_navigator.utils import error_and_exit_early

from ansible_navigator.configuration.parser import Parser
from ansible_navigator.configuration.definitions import EntrySource
from ansible_navigator.configuration.definitions import Message
from ansible_navigator.configuration.definitions import Config


class Configuration:
    def __init__(
        self,
        params,
        settings_file_path,
        application_configuration,
        apply_previous_cli=False,
        save_as_intitial=False,
    ):
        self._apply_previous_cli = apply_previous_cli
        self._config = application_configuration
        self._errors = []
        self._messages = []
        self._params = params
        self._save_as_intitial = save_as_intitial
        self._settings_file_path = settings_file_path
        self._sanity_check()
    
    def _sanity_check(self):
        if self._apply_previous_cli and self._save_as_intitial:
            raise ValueError("'apply_previous_cli' cannot be used with 'save_as_initial'")

    def configure(self):
        self._apply_defaults()
        self._apply_settings_file()
        self._apply_environment_variables()
        self._apply_cli_params()
        if self._errors:
            error_and_exit_early(errors=self._errors)

        self._post_process()
        if self._errors:
            error_and_exit_early(errors=self._errors)

        self._check_choices()
        if self._errors:
            error_and_exit_early(errors=self._errors)
        
        if self._apply_previous_cli:
            self._apply_previous_cli_to_current()
        
        if self._save_as_intitial:
            self._config.initial = deepcopy(self._config)

        return self._messages

    def _apply_defaults(self):
        for entry in self._config.entries:
            entry.value.current = entry.value.default
            entry.value.source = EntrySource.DEFAULT_CFG

    def _apply_settings_file(self):
        with open(self._settings_file_path, "r") as config_fh:
            try:
                config = yaml.load(config_fh, Loader=SafeLoader)
            except yaml.scanner.ScannerError:
                msg = f"Settings file found {self._settings_file_path}, but failed to load it."
                self._errors.append(msg)
                return
        for entry in self._config.entries:
            if entry.cli_parameters:
                settings_file_path = entry.settings_file_path(self._config.application_name)
                path_parts = settings_file_path.split(".")
                data = config
                try:
                    for key in path_parts:
                        data = data[key]
                    entry.value.current = data
                    entry.value.source = EntrySource.USER_CFG
                except KeyError:
                    msg = f"{settings_file_path} not found in settings file"
                    self._messages.append(Message(log_level="debug", message=msg))

    def _apply_environment_variables(self):
        for entry in self._config.entries:
            if entry.cli_parameters:
                set_envvar = os.environ.get(
                    entry.environment_variable(self._config.application_name)
                )
                if set_envvar is not None:
                    entry.value.current = set_envvar
                    entry.value.source = EntrySource.ENVIRONMENT_VARIABLE

    def _apply_cli_params(self):
        parser = Parser(self._config).parser
        args, cmdline = parser.parse_known_args(self._params)
        self._config.entry("cmdline").value.current = cmdline
        for param, value in vars(args).items():
            self._config.entry(param).value.current = value
            self._config.entry(param).value.source = EntrySource.USER_CLI

    def _post_process(self):
        for entry in self._config.entries:
            processor = getattr(self._config.post_processor, entry.name, None)
            if callable(processor):
                messages, errors = processor(entry=entry, config=self._config)
                self._messages.extend(messages)
                self._errors.extend(errors)

    def _check_choices(self):
        for entry in self._config.entries:
            if entry.cli_parameters and entry.choices:
                if entry.value.current not in entry.choices:
                    self._errors.append(entry.invalid_choice)
    
    def _apply_previous_cli_to_current(self):
        if self._config.initial is None:
            raise ValueError("'apply_previous_cli' enabled prior to 'save_as_initial'")
        for current_entry in self._config.entries:
            if current_entry.cli_parameters and current_entry.value.source.name != "USER_CLI":
                previous_entry = self._config.initial.entry(current_entry.name)
                if previous_entry.value.source.name == "USER_CLI":
                    current_entry.value.current = previous_entry.value.current
                    current_entry.value.source = EntrySource.PREVIOUS_CLI



    