"""Utilities related to the configuration subsystem."""
import logging

from configparser import ConfigParser
from configparser import ParsingError
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from ..command_runner import Command
from ..command_runner import CommandRunner
from ..utils.functions import ExitMessage
from ..utils.functions import LogMessage


SettingsFileSample = Dict[str, Union[Dict, str]]


def create_settings_file_sample(
    settings_path: str,
    placeholder: str = "",
) -> SettingsFileSample:
    """Generate a settings file sample.

    :param settings_path: The dot delimited settings file path for a settings entry
    :param placeholder: String used to identify the placement of a settings value
    :returns: A sample of the settings file
    """
    if "." not in settings_path:
        return {settings_path: placeholder}
    key, remainder = settings_path.split(".", 1)
    return {key: create_settings_file_sample(remainder, placeholder)}


def ansible_verison_parser(command: Command):
    """Parse the output of the ansible command.

    :param command: The result of running the command
    """
    if command.return_code:
        return

    messages: List[LogMessage] = []

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

    contents: Optional[Dict[str, Dict[str, Union[bool, int, float, str]]]] = None
    """The parsed contents of the file"""
    text: Optional[List[str]] = None
    """The text from the file"""
    path: Optional[Path] = None
    """The path to the file"""


@dataclass
class ParseAnsibleCfgResponse:
    """Data structure for the response of parse_ansible_cfg."""

    messages: List[LogMessage]
    """Log messages"""
    exit_messages: List[ExitMessage]
    """Exit messages"""
    config: AnsibleConfiguration = AnsibleConfiguration()
    """An ansible configuration"""


def parse_ansible_cfg(ee_enabled: bool) -> ParseAnsibleCfgResponse:
    """Find the ansible.cfg file and parse it.

    If running without an EE, use ansible to get it.
    If running with an EE only look in the CWD.
    In the future user-specified volume mounts might be considered as locations.

    :param ee_enabled: Indicates if EE support is enabled
    :returns: The ansible.cfg contents
    """
    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []

    if ee_enabled:
        cfg_path = Path.cwd() / "ansible.cfg"
        msg = f"EE support enabled, trying '$CWD': {cfg_path!s}"
        messages.append(LogMessage(level=logging.DEBUG, message=msg))

    else:
        new_messages, new_exit_messages, version_details = parse_ansible_verison()
        messages.extend(new_messages)
        exit_messages.extend(new_exit_messages)
        if exit_messages or version_details is None:
            return ParseAnsibleCfgResponse(messages=messages, exit_messages=exit_messages)

        cfg_file_name = version_details.get("config file")
        if cfg_file_name is None:
            msg = "No 'config file' in 'ansible --version'"
            messages.append(LogMessage(level=logging.DEBUG, message=msg))
            return ParseAnsibleCfgResponse(messages=messages, exit_messages=exit_messages)
        cfg_path = Path(cfg_file_name)
        msg = f"EE support disabled, trying 'ansible --version': {cfg_path}"
        messages.append(LogMessage(level=logging.DEBUG, message=msg))

    if not cfg_path.exists():
        msg = "{cfg_path} does not exist"
        messages.append(LogMessage(level=logging.DEBUG, message=msg))
        return ParseAnsibleCfgResponse(messages=messages, exit_messages=exit_messages)
    parser = ConfigParser()
    try:
        parser.read(str(cfg_path))
    except ParsingError as exc:
        exit_msg = f"The ansible configuration file '{cfg_path!s}' could not be parsed."
        exit_messages.append(ExitMessage(message=exit_msg))
        exit_messages.append(ExitMessage(message=str(exc)))
        return ParseAnsibleCfgResponse(messages=messages, exit_messages=exit_messages)

    return ParseAnsibleCfgResponse(
        messages=messages,
        exit_messages=exit_messages,
        config=AnsibleConfiguration(
            contents=parser.__dict__.get("_sections", {}),
            path=cfg_path,
            text=cfg_path.read_text(encoding="utf-8").splitlines(),
        ),
    )


def parse_ansible_verison() -> Tuple[List[LogMessage], List[ExitMessage], Optional[Dict[str, Any]]]:
    """Parse the output of the ansible --version command.

    :returns: Log messages, exit messages, and the stdout as a dictionary
    """
    messages: List[LogMessage] = []
    exit_messages: List[ExitMessage] = []

    command = Command(
        identity="ansible_version",
        command="ansible --version",
        post_process=ansible_verison_parser,
    )

    CommandRunner.run_single_proccess(commands=[command])
    if command.return_code:
        msg = "'ansible --version' reported the following errors:"
        exit_messages.append(ExitMessage(message=msg))
        exit_messages.append(ExitMessage(message=command.stderr))
        return messages, exit_messages, None

    msg = f"ansible --version stdout: '{command.stdout}'"
    messages.append(LogMessage(level=logging.DEBUG, message=msg))
    return messages, exit_messages, command.details[0]
