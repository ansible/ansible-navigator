"""The configuration object."""

from __future__ import annotations

import logging
import os

from copy import deepcopy

from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.definitions import ExitPrefix
from ansible_navigator.utils.definitions import LogMessage
from ansible_navigator.utils.functions import oxfordcomma
from ansible_navigator.utils.functions import shlex_join
from ansible_navigator.utils.json_schema import validate
from ansible_navigator.utils.serialize import SafeLoader
from ansible_navigator.utils.serialize import yaml
from ansible_navigator.utils.version_migration.migrate import MigrationType
from ansible_navigator.utils.version_migration.migrate import run_all_migrations

from .definitions import ApplicationConfiguration
from .definitions import Constants as C
from .definitions import SettingsEntry
from .parser import Parser
from .transform import to_schema
from .utils import parse_ansible_cfg


class Configurator:
    """The configuration class."""

    def __init__(
        self,
        params: list[str],
        application_configuration: ApplicationConfiguration,
        apply_previous_cli_entries: list | C = C.NONE,
        skip_roll_back: bool = False,
    ):
        """Initialize the configuration variables.

        :param params: A list of parameters e.g. ['-x', 'value']
        :param application_configuration: An application specific Config object
        :param apply_previous_cli_entries: Apply previous USER_CLI values where the current value
                                           is not a USER_CLI sourced value, a list of entry names
                                           ['all'] will apply all previous
        :param skip_roll_back: Skip roll back on error
        """
        self._apply_previous_cli_entries = apply_previous_cli_entries
        self._config = application_configuration
        self._exit_messages: list[ExitMessage] = []
        self._messages: list[LogMessage] = []
        self._params = params
        self._sanity_check()
        self._skip_rollback = skip_roll_back
        self._unaltered_entries = deepcopy(self._config.entries)

    def _sanity_check(self) -> None:
        """Sanity check the configuration.

        :raises ValueError: If apply_previous_cli is used while initializing
        """
        if self._apply_previous_cli_entries is not C.NONE:
            if self._config.internals.initializing:
                msg = "'apply_previous_cli' cannot be used while initializing"
                raise ValueError(msg)
            if not self._config.initial:
                msg = "'apply_previous_cli' enabled prior to an initialization"
                raise ValueError(msg)

    def _roll_back(self) -> None:
        """In the case of a rollback, log the configuration state prior to roll back."""
        if self._skip_rollback:
            return
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

    def configure(self) -> tuple[list[LogMessage], list[ExitMessage]]:
        """Perform the configuration.

        Save the original entries, if an error is encountered
        restore them.

        :returns: Log messages
        """
        self._config.original_command = self._params
        shlex_joined = shlex_join(self._config.original_command)
        cmd_message = f"Command provided: '{shlex_joined}'"
        self._messages.append(LogMessage(level=logging.DEBUG, message=cmd_message))
        warn_message = "Issues were found while applying the settings."
        warning = ExitMessage(message=warn_message, prefix=ExitPrefix.WARNING)
        command = ExitMessage(message=cmd_message, prefix=ExitPrefix.HINT)

        self._restore_original()
        self._apply_defaults()
        self._apply_settings_file()
        self._apply_environment_variables()
        self._apply_cli_params()
        if self._exit_messages:
            self._exit_messages[0:0] = [warning, command]
            self._roll_back()
            return self._messages, self._exit_messages

        self._apply_previous_cli_to_current()

        self._retrieve_ansible_cfg()
        self._post_process()
        self._check_choices()
        if self._exit_messages:
            self._exit_messages[0:0] = [warning, command]
            self._roll_back()
            return self._messages, self._exit_messages

        if self._config.internals.initializing:
            self._config.initial = deepcopy(self._config)
            # Our work is done, set the initialization flag to false
            self._config.internals.initializing = False

        return self._messages, self._exit_messages

    def _argparse_error_handler(self, message: str):
        """Call back for argparser error handling.

        :param message: A message from the parser
        :type message: str
        """
        self._exit_messages.append(ExitMessage(message=message))

    def _restore_original(self) -> None:
        """Restore the current values back to NOT_SET."""
        for entry in self._config.entries:
            if self._config.internals.initializing or entry.change_after_initial:
                entry.value.current = C.NOT_SET
                entry.value.source = C.NOT_SET
            else:
                message = f"'{entry.name}' cannot be reconfigured. (restore original)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _apply_defaults(self) -> None:
        """Apply the default values."""
        for entry in self._config.entries:
            if self._config.internals.initializing or entry.change_after_initial:
                if entry.value.default is not C.NOT_SET:
                    entry.value.current = entry.value.default
                    entry.value.source = C.DEFAULT_CFG
            else:
                message = f"'{entry.name}' cannot be reconfigured. (apply defaults)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _apply_settings_file(self) -> None:
        # pylint: disable=too-many-locals
        """Apply the settings file.

        :raises ValueError: If the settings file is empty
        """
        settings_filesystem_path = self._config.internals.settings_file_path

        if not isinstance(settings_filesystem_path, str):
            return

        run_all_migrations(
            settings_file_str=settings_filesystem_path,
            migration_types=(MigrationType.SETTINGS_FILE,),
        )

        with open(settings_filesystem_path, encoding="utf-8") as fh:
            try:
                config = yaml.load(fh, Loader=SafeLoader)
                if config is None:
                    # In the case of ansible-navigator settings --sample > ansible-navigator.yml
                    # the file will be empty, but we shouldn't exit.
                    if self._params in (["settings", "--sample"], ["settings", "--gs"]):
                        return
                    msg = "Settings file cannot be empty."
                    raise ValueError(msg)
            except (yaml.scanner.ScannerError, yaml.parser.ParserError, ValueError) as exc:
                exit_msg = f"Settings file found {settings_filesystem_path}, but failed to load it."
                self._exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = f"  error was: '{' '.join(str(exc).splitlines())}'"
                self._exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = (
                    f"Try checking the settings file '{settings_filesystem_path}'"
                    "and ensure it is properly formatted"
                )
                self._exit_messages.append(
                    ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT),
                )
                return

        schema = to_schema(settings=self._config)
        errors = validate(schema=schema, data=config)

        if errors:
            msg = (
                "The following errors were found in the settings file"
                f" ({settings_filesystem_path}):"
            )
            self._exit_messages.append(ExitMessage(message=msg))
            self._exit_messages.extend(error.to_exit_message() for error in errors)
            hint = "Check the settings file and compare it to the current version."
            self._exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))
            hint = (
                "The current version can be found here:"
                " (https://ansible-navigator.readthedocs.io/en/latest/settings/"
                "#ansible-navigator-settings)"
            )
            self._exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))
            hint = (
                "The schema used for validation can be seen with"
                " 'ansible-navigator settings --schema'"
            )
            self._exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))
            hint = (
                "A sample settings file can be created with"
                " 'ansible-navigator settings --sample'"
            )
            self._exit_messages.append(ExitMessage(message=hint, prefix=ExitPrefix.HINT))
            return

        for entry in self._config.entries:
            settings_file_path = entry.settings_file_path(self._config.application_name)
            path_parts = settings_file_path.split(".")
            data = config
            try:
                for key in path_parts:
                    data = data[key]
                if self._config.internals.initializing or entry.change_after_initial:
                    entry.value.current = data
                    entry.value.source = C.USER_CFG
                else:
                    message = f"'{entry.name}' cannot be reconfigured. (settings file)"
                    self._messages.append(LogMessage(level=logging.INFO, message=message))
            except TypeError as exc:
                exit_msg = (
                    "Errors encountered when loading settings file:"
                    f" {settings_filesystem_path}"
                    f" while loading entry {entry.name}, attempted: {settings_file_path}."
                    f"The resulting error was {exc!s}"
                )
                self._exit_messages.append(ExitMessage(message=exit_msg))
                exit_msg = (
                    f"Try checking the settings file '{settings_filesystem_path}'"
                    "and ensure it is properly formatted"
                )
                self._exit_messages.append(
                    ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT),
                )
                return
            except KeyError:
                message = f"{settings_file_path} not found in settings file"
                self._messages.append(LogMessage(level=logging.DEBUG, message=message))

    def _apply_environment_variables(self) -> None:
        """Apply the environment variables."""
        for entry in self._config.entries:
            set_env_var = os.environ.get(entry.environment_variable(self._config.application_name))
            if set_env_var is not None:
                if self._config.internals.initializing or entry.change_after_initial:
                    if entry.cli_parameters is not None and entry.cli_parameters.nargs in [
                        "+",
                        "*",
                    ]:
                        entry.value.current = [
                            value.strip()
                            for value in set_env_var.split(entry.environment_variable_split_char)
                        ]
                    else:
                        entry.value.current = set_env_var
                    entry.value.source = C.ENVIRONMENT_VARIABLE
                else:
                    message = f"'{entry.name}' cannot be reconfigured. (environment variables)"
                    self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _apply_cli_params(self) -> None:
        """Apply the cli params."""
        parser = Parser(self._config).parser
        setattr(parser, "error", self._argparse_error_handler)
        try:
            # split the _params on double-dash
            index = self._params.index("--")
            before, after = self._params[:index], self._params[index + 1 :]
        except ValueError:
            before, after = self._params, []

        parser_response = parser.parse_known_args(before)
        if parser_response is None:
            return
        args, unknown = parser_response
        cmdline = unknown + after
        if cmdline:
            # In the case a subcommand is not a positional, remove the --
            additional_args = [arg for arg in cmdline if arg != "--"]
            self._config.entry("cmdline").value.current = additional_args
            self._config.entry("cmdline").value.source = C.USER_CLI
        for param, value in vars(args).items():
            if self._config.entry(param).subcommand_value is True and value is None:
                continue
            entry = self._config.entry(param)
            if self._config.internals.initializing or entry.change_after_initial:
                entry.value.current = value
                entry.value.source = C.USER_CLI
            else:
                message = f"'{entry.name}' cannot be reconfigured. (cli params)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _post_process(self) -> None:
        """Post process the settings entries."""
        delayed = []
        normal = []

        # Separate normal and delayed entries so they can be processed in that order.
        for entry in self._config.entries:
            if entry.delay_post_process:
                delayed.append(entry)
            else:
                normal.append(entry)

        for entry in normal + delayed:
            if self._config.internals.initializing or entry.change_after_initial:
                processor = getattr(self._config.post_processor, entry.name, None)
                if callable(processor):
                    messages, errors = processor(entry=entry, config=self._config)
                    self._messages.extend(messages)
                    self._exit_messages.extend(errors)
            else:
                message = f"'{entry.name}' cannot be reconfigured. (post process)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))

    def _check_choices(self) -> None:
        """Check the choices for each settings entry."""
        for entry in self._config.entries:
            if entry.cli_parameters and entry.choices:
                if isinstance(entry.value.current, list):
                    for value in entry.value.current:
                        logged = self._check_choice(entry=entry, value=value)
                        if logged:
                            break
                else:
                    self._check_choice(entry=entry, value=entry.value.current)

    def _check_choice(self, entry: SettingsEntry, value: bool | str):
        """Check the choice for a single settings entry.

        :param entry: The settings entry to check.
        :param value: The value to check.
        :return: True if the value is invalid and an error message was logged.
        """
        if entry.cli_parameters and entry.choices and value not in entry.choices:
            self._exit_messages.append(ExitMessage(message=entry.invalid_choice))
            choices = [
                f"{entry.cli_parameters.short} {str(choice).lower()}" for choice in entry.choices
            ]
            exit_msg = f"Try again with {oxfordcomma(choices, 'or')}"
            self._exit_messages.append(
                ExitMessage(message=exit_msg, prefix=ExitPrefix.HINT),
            )
            return True
        return False

    def _apply_previous_cli_to_current(self) -> None:
        """Apply eligible previous CLI values to current not set by the CLI."""
        # _apply_previous_cli_entries must be ALL or a list of entries
        if self._apply_previous_cli_entries is not C.ALL and not isinstance(
            self._apply_previous_cli_entries,
            list,
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
            # retrieve the corresponding previous entry
            previous_entry = self._config.initial.entry(current_entry.name)

            # skip if not initial and not able to be changed
            if not any((self._config.internals.initializing, current_entry.change_after_initial)):
                message = f"'{current_entry.name}' cannot be reconfigured (apply previous cli)"
                self._messages.append(LogMessage(level=logging.INFO, message=message))
                continue

            # skip if currently set from the CLI
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
            if (
                current_entry.apply_to_subsequent_cli is C.SAME_SUBCOMMAND
                and current_subcommand != previous_subcommand
            ):
                continue

            # skip if the previous entry was not set by the CLI
            if previous_entry.value.source is not C.USER_CLI:
                continue

            current_entry.value.current = previous_entry.value.current
            current_entry.value.source = C.PREVIOUS_CLI

    def _retrieve_ansible_cfg(self):
        """Retrieve the ansible.cfg file.

        EE support is needed early on here so the post processors
        can have access to the ansible.cfg file contents as a fallback to
        navigators settings sources. The value won't be set but it is needed to
        determine where the ansible.cfg file should be pulled from
        """
        ee_enabled = str(self._config.execution_environment).lower() == "true"
        parsed_ansible_cfg = parse_ansible_cfg(ee_enabled=ee_enabled)
        self._messages.extend(parsed_ansible_cfg.messages)
        self._exit_messages.extend(parsed_ansible_cfg.exit_messages)
        self._config.internals.ansible_configuration = parsed_ansible_cfg.config
