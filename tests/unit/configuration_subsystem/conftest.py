"""Fixtures for configuration subsystem tests."""
from __future__ import annotations

import os

from copy import deepcopy
from typing import NamedTuple

import pytest

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner.command_runner import run_command
from ansible_navigator.configuration_subsystem import to_schema
from ansible_navigator.configuration_subsystem.configurator import Configurator
from ansible_navigator.configuration_subsystem.definitions import (
    ApplicationConfiguration,
)
from ansible_navigator.configuration_subsystem.definitions import SettingsSchemaType
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    NavigatorConfiguration,
)
from ansible_navigator.utils.functions import ExitMessage
from ansible_navigator.utils.functions import LogMessage
from ansible_navigator.utils.serialize import Loader
from ansible_navigator.utils.serialize import yaml
from ...defaults import FIXTURES_DIR


TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "unit", "configuration_subsystem")


class GenerateConfigResponse(NamedTuple):
    """Object for generate_config_response."""

    messages: list[LogMessage]
    exit_messages: list[ExitMessage]
    application_configuration: ApplicationConfiguration
    settings_contents: dict


def _generate_config(params=None, setting_file_name=None, initial=True) -> GenerateConfigResponse:
    """Generate a configuration given a settings file.

    :param initial: Bool for if this is the first run
    :param setting_file_name: Name of settings file name
    :param params: Configuration parameters
    :returns: Generated config response object
    """
    if params is None:
        params = []

    if setting_file_name:
        settings_file_path = os.path.join(TEST_FIXTURE_DIR, setting_file_name)
        with open(file=settings_file_path, encoding="utf-8") as fh:
            try:
                settings_contents = yaml.load(fh, Loader=Loader)
            except yaml.parser.ParserError:
                # let the configuration subsystem catch the invalid yaml file
                settings_contents = {}
    else:
        settings_file_path = ""
        settings_contents = {}

    # make a deep copy here to ensure we do not modify the original
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = initial
    application_configuration.application_version = "test"
    application_configuration.internals.settings_file_path = settings_file_path or None
    configurator = Configurator(
        application_configuration=application_configuration,
        params=params,
    )
    messages, exit_messages = configurator.configure()
    return GenerateConfigResponse(
        messages=messages,
        exit_messages=exit_messages,
        application_configuration=application_configuration,
        settings_contents=settings_contents,
    )


@pytest.fixture(name="generate_config")
def fixture_generate_config():
    """Generate a configuration.

    :returns: A generated config
    """
    return _generate_config


@pytest.fixture
def ansible_version(monkeypatch):
    """Path the ansible --version call to avoid the subprocess calls.

    :param monkeypatch: Fixture for patching
    """
    original_run_command = run_command

    def static_ansible_version(command: Command):
        if command.command == "ansible --version":
            command.return_code = 0
            command.stdout = "ansible [core 2.12.3]\nconfig file = None"
        else:
            original_run_command(command)

    monkeypatch.setattr(
        "ansible_navigator.command_runner.command_runner.run_command",
        static_ansible_version,
    )


@pytest.fixture(name="schema_dict")
def _schema_dict() -> SettingsSchemaType:
    """Provide the json schema as a dictionary.

    :returns: the json schema as a dictionary
    """
    settings = deepcopy(NavigatorConfiguration)
    settings.application_version = "test"
    schema = to_schema(settings)
    return SettingsSchemaType(schema)


@pytest.fixture()
def schema_dict_all_required(schema_dict: SettingsSchemaType) -> SettingsSchemaType:
    """Provide the json schema as a dictionary with all properties required.

    :param schema_dict: The schema dictionary
    :returns: the json schema as a dictionary
    """

    def property_dive(subschema: dict):
        if "properties" in subschema:
            subschema["required"] = list(subschema["properties"].keys())
            for value in subschema["properties"].values():
                property_dive(subschema=value)

    property_dive(schema_dict)
    return schema_dict
