"""Tests for the transformation of settings to a presentable structure."""

from dataclasses import asdict

import pytest

from ansible_navigator.configuration_subsystem import ApplicationConfiguration
from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.configuration_subsystem import PresentableSettingsEntry
from ansible_navigator.configuration_subsystem import SettingsEntry
from ansible_navigator.configuration_subsystem import to_presentable
from ansible_navigator.configuration_subsystem.definitions import CliParameters
from ansible_navigator.configuration_subsystem.definitions import SettingsEntryValue
from ansible_navigator.configuration_subsystem.definitions import SubCommand
from ansible_navigator.configuration_subsystem.navigator_configuration import Internals
from ansible_navigator.configuration_subsystem.navigator_post_processor import (
    NavigatorPostProcessor,
)


@pytest.fixture(name="sample_settings")
def _sample_settings():
    return ApplicationConfiguration(
        application_name="app",
        application_version="1.0",
        internals=Internals(settings_file_path="/test/path"),
        post_processor=NavigatorPostProcessor(),
        subcommands=[
            SubCommand(name="subcommand_1", description="subcommand_1"),
        ],
        entries=[],
    )


@pytest.fixture(name="settings_file_dict")
def _settings_file_dict():
    return {
        "choices": [],
        "current_settings_file": "/test/path",
        "current_value": "/test/path",
        "default_value": "None",
        "default": False,
        "description": (
            "The path to the current settings file. Possible locations are"
            " {CWD}/ansible-navigator.{ext} or {HOME}/.ansible-navigator.{ext}"
            " where ext is yml, yaml or json."
        ),
        "env_var": "APP_CONFIG",
        "name": "Current settings file",
        "settings_file_sample": "Not applicable",
        "source": "Not set",
        "subcommands": ["subcommand_1"],
        "cli_parameters": {"long": "No long CLI parameter", "short": "No short CLI parameter"},
    }


def test_settings_file_entry(sample_settings, settings_file_dict):
    """Ensure the settings file entry is properly constructed.

    :param sample_settings: A sample application configuration (settings)
    :param settings_file_dict: The expected settings as a dictionary
    """
    configurator = Configurator(params=[], application_configuration=sample_settings)
    configurator._post_process()  # pylint: disable=protected-access
    presentable = to_presentable(sample_settings)
    # pylint: disable=not-an-iterable # https://github.com/PyCQA/pylint/issues/2296
    assert all(isinstance(p, PresentableSettingsEntry) for p in presentable)
    assert asdict(presentable[0]) == settings_file_dict


def test_settings_entry(sample_settings, settings_file_dict):
    """Ensure a settings entry is properly constructed.

    :param sample_settings: A sample application configuration (settings)
    :param settings_file_dict: The expected settings as a dictionary
    """
    entry = SettingsEntry(
        name="se_1",
        choices=["choice_1", "choice_2"],
        cli_parameters=CliParameters(short="-se1"),
        short_description="description",
        value=SettingsEntryValue(
            current="current",
            default="default",
            source=Constants.ENVIRONMENT_VARIABLE,
        ),
    )
    sample_settings.entries = [entry]
    configurator = Configurator(params=[], application_configuration=sample_settings)
    configurator._post_process()  # pylint: disable=protected-access
    presentable = to_presentable(sample_settings)
    # pylint: disable=not-an-iterable # https://github.com/PyCQA/pylint/issues/2296
    assert all(isinstance(p, PresentableSettingsEntry) for p in presentable)
    assert asdict(presentable[0]) == settings_file_dict
    entry_dict = {
        "choices": ["choice_1", "choice_2"],
        "current_settings_file": "/test/path",
        "current_value": "current",
        "default_value": "default",
        "default": False,
        "description": "description",
        "env_var": "APP_SE_1",
        "name": "Se 1",
        "settings_file_sample": {"app": {"se-1": "<------"}},
        "source": "Environment variable",
        "subcommands": ["subcommand_1"],
        "cli_parameters": {"long": "--se-1", "short": "-se1"},
    }
    assert asdict(presentable[1]) == entry_dict
