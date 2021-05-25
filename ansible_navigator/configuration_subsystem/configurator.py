""" The configuration object
"""
import logging
import os
import shlex

from copy import deepcopy
from typing import List
from typing import Tuple
from typing import Union

from .definitions import ApplicationConfiguration
from .definitions import Constants as C
from .parser import Parser

from ..utils import ExitMessage
from ..utils import ExitPrefix
from ..utils import LogMessage
from ..utils import oxfordcomma
from ..yaml import SafeLoader
from ..yaml import yaml


class Configurator:
    # pylint: disable=too-many-arguments
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    """the configuration class"""

    def __init__(
        self,
        params: List[str],
        application_configuration: ApplicationConfiguration,
        apply_previous_cli_entries: Union[List, C] = C.NONE,
        initial: bool = False,
        settings_file_path: str = None,
    ):
        """
        :param params: A list of parameters ie ['-x', 'value']
        :param application_configuration: An application specific Config object
        :param apply_previous_cli_entries: Apply previous USER_CLI values where the current value
                                           is not a USER_CLI sourced value, a list of entry names
                                           ['all'] will apply all previous
        :param initial: Save the resulting configuration as the 'initial' configuration
                        The 'initial' will be used as a source for apply_previous_cli
        :param settings_file_path: The full path to a settings file
        """
        self._apply_previous_cli_entries = apply_previous_cli_entries
        self._config = application_configuration
        self._exit_messages: List[ExitMessage] = []
        self._messages: List[LogMessage] = []
        self._params = params
        self._initial = initial
        self._settings_file_path = settings_file_path
        self._sanity_check()
        self._unaltered_entries = deepcopy(self._config.entries)

    def _sanity_check(self) -> None:
        if self._apply_previous_cli_entries is not C.NONE:
            if self._initial is True:
                raise ValueError("'apply_previous_cli' cannot be used with 'initial'")
            if self._config.initial is None:
                raise ValueError("'apply_previous_cli' enabled prior to 'initial'")

    def _roll_back(self) -> None:
        """In the case of a rollback, log the configuration state
        prior to roll back
        """
        message = "Configuration errors encountered, rolling back to previous configuration."
        self._messages.append(LogMessage(level=logging.WARNING, message=message))
        for entry in self._config.entries:
            message = f"Prior to rollback: {entry.name} = '{entry.value.current}'"
            message += f" ({type(entry.value.current).__name__}/{entry.value.source.value})"
            self._messages.append(LogMessage(level=logging.DEBUG, message=message))
        self._config.entries = self._unaltered_entries
        for entry in self._config.entries:
            message = f"After rollback: {entry.name} = '{entry.value.current}'"
            message += f" ({type(entry.value.current).__name__}/{entry.value.source.value})"
            self._messages.append(LogMessage(level=logging.DEBUG, message=message))
        message = "Configuration rollback complete."
        self._messages.append(LogMessage(level=logging.DEBUG, message=message))

    def configure(self) -> Tuple[List[LogMessage], List[ExitMessage]]:
        """Perform the configuration

        save the original entries, if an error is encountered
        restore them
        """
        self._config.original_command = self._params
        shlex_joined = " ".join(shlex.quote(arg) for arg in self._config.original_command)
        cmd_message = f"Command provided: '{shlex_joined}'"
        self._messages.append(LogMessage(level=logging.DEBUG, message=cmd_message))

        self._restore_original()
        self._apply_defaults()
        self._apply_settings_file()
        self._apply_environment_variables()
        self._apply_cli_params()
        if self._exit_messages:
            self._exit_messages.insert(0, ExitMessage(message=cmd_message))
            self._roll_back()
            return self._messages, self._exit_messages

        self._apply_previous_cli_to_current()

        self._post_process()
        self._check_choices()
        if self._exit_messages:
            self._exit_messages.insert(0, ExitMessage(message=cmd_message))
            self._roll_back()
            return self._messages, self._exit_messages

        if self._initial:
            self._config.initial = deepcopy(self._config)

        return self._messages, self._exit_messages

    def _argparse_error_handler(self, message: str):
        """callback for argparse error handling to prevent sys.exit

        :param message: A message from the parser
        :type message: str
        """
        self._exit_messages.append(ExitMessage(message=message))

    def _restore_original(self) -> None:
        """Since we always operate on the same object
        restore the current values back to NOT_SET
        """
        for entry in self._config.entries:
            if self._initial or entry.change_after_initial:
                entry.value.current = C.NOT_SET
                entry.value.source = C.NOT_SET
            else:
                message = f"'{entry.name}' cannot be reconfigured. (restore original)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _apply_defaults(self) -> None:
        for entry in self._config.entries:
            if self._initial or entry.change_after_initial:
                if entry.value.default is not C.NOT_SET:
                    entry.value.current = entry.value.default
                    entry.value.source = C.DEFAULT_CFG
            else:
                message = f"'{entry.name}' cannot be reconfigured. (apply defaults)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _apply_settings_file(self) -> None:
        if self._settings_file_path:
            with open(self._settings_file_path, "r") as config_fh:
                try:
                    config = yaml.load(config_fh, Loader=SafeLoader)
                except (yaml.scanner.ScannerError, yaml.parser.ParserError) as exc:
                    exit_msg = (
                        f"Settings file found {self._settings_file_path}, but failed to load it."
                    )
                    self._exit_messages.append(ExitMessage(message=exit_msg))
                    exit_msg = f"  error was: '{' '.join(str(exc).splitlines())}'"
                    self._exit_messages.append(ExitMessage(message=exit_msg))
                    exit_msg = (
                        f"Try checking the settings file '{self._settings_file_path}'"
                        "and ensure it is properly formatted"
                    )
                    self._exit_messages.append(
                        ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT)
                    )
                    return
            for entry in self._config.entries:
                settings_file_path = entry.settings_file_path(self._config.application_name)
                path_parts = settings_file_path.split(".")
                data = config
                try:
                    for key in path_parts:
                        data = data[key]
                    if self._initial or entry.change_after_initial:
                        entry.value.current = data
                        entry.value.source = C.USER_CFG
                    else:
                        message = f"'{entry.name}' cannot be reconfigured. (settings file)"
                        self._messages.append(LogMessage(level=logging.INFO, message=message))
                except TypeError as exc:
                    exit_msg = (
                        "Errors encountered when loading settings file:"
                        f" {self._settings_file_path}"
                        f" while loading entry {entry.name}, attempted: {settings_file_path}."
                        f"The resulting error was {str(exc)}"
                    )
                    self._exit_messages.append(ExitMessage(message=exit_msg))
                    exit_msg = (
                        f"Try checking the settings file '{self._settings_file_path}'"
                        "and ensure it is properly formatted"
                    )
                    self._exit_messages.append(
                        ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT)
                    )
                    return
                except KeyError:
                    message = f"{settings_file_path} not found in settings file"
                    self._messages.append(LogMessage(level=logging.DEBUG, message=message))

    def _apply_environment_variables(self) -> None:
        for entry in self._config.entries:
            set_envvar = os.environ.get(entry.environment_variable(self._config.application_name))
            if set_envvar is not None:
                if self._initial or entry.change_after_initial:
                    if entry.cli_parameters is not None and entry.cli_parameters.nargs == "+":
                        entry.value.current = set_envvar.split(",")
                    else:
                        entry.value.current = set_envvar
                    entry.value.source = C.ENVIRONMENT_VARIABLE
                else:
                    message = f"'{entry.name}' cannot be reconfigured. (environment variables)"
                    self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _apply_cli_params(self) -> None:
        parser = Parser(self._config).parser
        setattr(parser, "error", self._argparse_error_handler)
        parser_response = parser.parse_known_args(self._params)
        if parser_response is None:
            return
        args, cmdline = parser_response
        if cmdline:
            self._config.entry("cmdline").value.current = cmdline
            self._config.entry("cmdline").value.source = C.USER_CLI
        for param, value in vars(args).items():
            if self._config.entry(param).subcommand_value is True and value is None:
                continue
            entry = self._config.entry(param)
            if self._initial or entry.change_after_initial:
                entry.value.current = value
                entry.value.source = C.USER_CLI
            else:
                message = f"'{entry.name}' cannot be reconfigured. (cli params)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _post_process(self) -> None:
        for entry in self._config.entries:
            if self._initial or entry.change_after_initial:
                processor = getattr(self._config.post_processor, entry.name, None)
                if callable(processor):
                    messages, errors = processor(entry=entry, config=self._config)
                    self._messages.extend(messages)
                    self._exit_messages.extend(errors)
            else:
                message = f"'{entry.name}' cannot be reconfigured. (post process)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _check_choices(self) -> None:
        for entry in self._config.entries:
            if entry.cli_parameters and entry.choices:
                if entry.value.current not in entry.choices:
                    self._exit_messages.append(ExitMessage(message=entry.invalid_choice))
                    choices = [
                        f"{entry.cli_parameters.short} {str(choice).lower()}"
                        for choice in entry.choices
                    ]
                    exit_msg = f"Try again with {oxfordcomma(choices, 'or')}"
                    self._exit_messages.append(
                        ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT)
                    )

    def _apply_previous_cli_to_current(self) -> None:
        # pylint: disable=too-many-nested-blocks
        """Apply eligible previous cli values to current not set by the cli"""

        # _apply_previous_cli_entries must be ALL or a list of entries
        if self._apply_previous_cli_entries is not C.ALL and not isinstance(
            self._apply_previous_cli_entries, list
        ):
            return

        current_subcommand = [
            entry.value.current for entry in self._config.entries if entry.subcommand_value is True
        ][0]
        previous_subcommand = [
            entry.value.current
            for entry in self._config.initial.entries
            if entry.subcommand_value is True
        ][0]

        for current_entry in self._config.entries:
            # retrieve the correspoding previous entry
            previous_entry = self._config.initial.entry(current_entry.name)

            # skip if not initial and not able to be changed
            if not any((self._initial, current_entry.change_after_initial)):
                message = f"'{current_entry.name}' cannot be reconfigured (apply previous cli)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))
                continue

            # skip if currently set from the cli
            if current_entry.value.source is C.USER_CLI:
                continue

            # skip if _apply_previous_cli_entries is a list and the entry isn't in it
            if (
                isinstance(self._apply_previous_cli_entries, list)
                and current_entry.name not in self._apply_previous_cli_entries
            ):
                continue

            # skip if the previous entry not eligible for reapplication
            if previous_entry.apply_to_subsequent_cli not in [C.ALL, C.SAME_SUBCOMMAND]:
                continue

            # skip if the same subcommand is required for reapplication
            if current_entry.apply_to_subsequent_cli is C.SAME_SUBCOMMAND:
                if current_subcommand != previous_subcommand:
                    continue

            # skip if the previous entry was not set by the cli
            if previous_entry.value.source is not C.USER_CLI:
                continue

            current_entry.value.current = previous_entry.value.current
            current_entry.value.source = C.PREVIOUS_CLI
