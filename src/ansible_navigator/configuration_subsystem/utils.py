"""Utilities related to the configuration subsystem."""
from __future__ import annotations

import logging

from configparser import ConfigParser
from configparser import ParsingError
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner import CommandRunner
from ansible_navigator.utils.definitions import ExitMessage
from ansible_navigator.utils.definitions import LogMessage

from .definitions import Constants
from .definitions import SettingsFileType


def create_settings_file_sample(
    settings_path: str,
    placeholder: bool | int | str | dict | list = "",
) -> SettingsFileType:
    """Generate a settings file sample.

    :param settings_path: The dot delimited settings file path for a settings entry
    :param placeholder: String used to identify the placement of a settings value
    :returns: A sample of the settings file
    """
    if "." not in settings_path:
        return SettingsFileType({settings_path: placeholder})
    key, remainder = settings_path.split(".", 1)
    return SettingsFileType({key: create_settings_file_sample(remainder, placeholder)})


def ansible_verison_parser(command: Command):
    """Parse the output of the ansible command.

    :param command: The result of running the command
    """
    if command.return_code:
        return

    messages: list[LogMessage] = []

    details = {}
    # First line contains the version
    version = command.stdout_lines[0].split(" ", 1)[1].strip()[1:-1]
    details["version"] = version
    # Remaining lines are k = v pairs
    for entry in command.stdout_lines[1:]:
        parts = entry.split("=")
        if len(parts) == 2:
            details[parts[0].strip()] = parts[1].strip()
        else:
            msg = "ansible --version entry: '{entry}' could not be parsed"
            messages.append(LogMessage(level=logging.ERROR, message=msg))

    for key, value in details.items():
        msg = f"ansible --version: '{key}:{value}'"
        messages.append(LogMessage(level=logging.ERROR, message=msg))

    command.details = [details]
    command.messages = messages


@dataclass
class AnsibleConfiguration:
    """Data structure for an ansible.cfg file."""

    contents: (Constants | dict[str, dict[str, bool | int | float | str]]) = Constants.NOT_SET
    """The parsed contents of the file"""
    text: Constants | list[str] = Constants.NOT_SET
    """The text from the file"""
    path: Constants | Path = Constants.NOT_SET
    """The path to the file"""


@dataclass
class ParseAnsibleCfgResponse:
    """Data structure for the response of parse_ansible_cfg."""

    messages: list[LogMessage]
    """Log messages"""
    exit_messages: list[ExitMessage]
    """Exit messages"""
    config: AnsibleConfiguration = field(default_factory=AnsibleConfiguration)
    """An ansible configuration"""


def parse_ansible_cfg(ee_enabled: bool) -> ParseAnsibleCfgResponse:
    """Find the ansible.cfg file and parse it.

    If running without an EE, use ansible to get it.
    If running with an EE only look in the CWD.
    In the future user-specified volume mounts might be considered as locations.

    :param ee_enabled: Indicates if EE support is enabled
    :returns: The ansible.cfg contents
    """
    response = ParseAnsibleCfgResponse(messages=[], exit_messages=[])
    response.config.path = Constants.NONE
    response.config.text = Constants.NONE
    response.config.contents = Constants.NONE

    if ee_enabled:
        msg = "EE support enabled: using current working directory for 'ansible.cfg'"
        response.messages.append(LogMessage(level=logging.DEBUG, message=msg))
        cfg_path = Path.cwd() / "ansible.cfg"
        if not cfg_path.exists():
            msg = (
                "EE support enabled: no 'ansible.cfg' found in current working directory."
                f" Tried {cfg_path!s}"
            )
            response.messages.append(LogMessage(level=logging.INFO, message=msg))
            return response

        msg = "EE support enabled: found 'ansible.cfg' in current working directory."
        response.messages.append(LogMessage(level=logging.INFO, message=msg))

    else:
        msg = "EE support disabled: using 'ansible --version' for 'ansible.cfg'"
        response.messages.append(LogMessage(level=logging.DEBUG, message=msg))
        new_messages, new_exit_messages, version_details = parse_ansible_verison()
        response.messages.extend(new_messages)
        response.exit_messages.extend(new_exit_messages)
        if response.exit_messages or version_details is None:
            return response

        cfg_file_name = version_details.get("config file")
        if cfg_file_name is None:
            msg = "EE support disabled: no 'config file' in 'ansible --version'"
            response.messages.append(LogMessage(level=logging.DEBUG, message=msg))
            return response
        if cfg_file_name == "None":
            msg = "EE support disabled: 'ansible --version' reports no config file"
            response.messages.append(LogMessage(level=logging.INFO, message=msg))
            return response
        cfg_path = Path(cfg_file_name)
        if not cfg_path.exists():
            msg = f"EE support disabled: {cfg_path!s} does not exist"
            response.messages.append(LogMessage(level=logging.DEBUG, message=msg))
            return response

    parser = ConfigParser()
    try:
        parser.read(str(cfg_path))
    except ParsingError as exc:
        exit_msg = f"The ansible configuration file '{cfg_path!s}' could not be parsed."
        response.exit_messages.append(ExitMessage(message=exit_msg))
        response.exit_messages.append(ExitMessage(message=str(exc)))
        return response

    response.config.contents = parser.__dict__.get("_sections", {})
    response.config.path = cfg_path
    response.config.text = cfg_path.read_text(encoding="utf-8").splitlines()
    return response


def parse_ansible_verison() -> tuple[list[LogMessage], list[ExitMessage], dict[str, Any] | None]:
    """Parse the output of the ansible --version command.

    :returns: Log messages, exit messages, and the stdout as a dictionary
    """
    messages: list[LogMessage] = []
    exit_messages: list[ExitMessage] = []

    command = Command(
        identity="ansible_version",
        command="ansible --version",
        post_process=ansible_verison_parser,
    )

    CommandRunner.run_single_process(commands=[command])
    if command.return_code:
        msg = "'ansible --version' reported the following errors:"
        exit_messages.append(ExitMessage(message=msg))
        exit_messages.append(ExitMessage(message=command.stderr))
        return messages, exit_messages, None

    msg = f"ansible --version stdout: '{command.stdout}'"
    messages.append(LogMessage(level=logging.DEBUG, message=msg))
    return messages, exit_messages, command.details[0]
