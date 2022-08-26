"""Test the ability to recreate a settings file post configuration."""
from __future__ import annotations

import operator

from copy import deepcopy
from functools import reduce
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem import SettingsFileType
from ansible_navigator.configuration_subsystem import SettingsSchemaType
from ansible_navigator.configuration_subsystem import to_effective
from ansible_navigator.initialization import parse_and_update
from ansible_navigator.utils.functions import abs_user_path
from ansible_navigator.utils.json_schema import validate


def test_defaults(schema_dict: SettingsSchemaType):
    """Check the settings file used as a sample against the schema.

    :param schema_dict: The json schema as a dictionary
    """
    settings = deepcopy(NavigatorConfiguration)
    settings.internals.initializing = True
    Configurator(params=[], application_configuration=settings).configure()

    effective = to_effective(settings)
    errors = validate(schema=schema_dict, data=effective)
    assert not errors


def test_settings_env_var_to_full(
    settings_env_var_to_full: tuple[Path, SettingsFileType],
):
    """Confirm the fixture writes the file and environment variable.

    :param settings_env_var_to_full: The env var and file writing fixture
    """
    settings_path, _sample = settings_env_var_to_full

    settings = deepcopy(NavigatorConfiguration)
    settings.internals.initializing = True
    _messages, exit_messages = parse_and_update(params=[], args=settings)

    # Some sanity checking
    assert not exit_messages
    assert settings.internals.settings_file_path == str(settings_path)
    assert settings.internals.settings_source == Constants.ENVIRONMENT_VARIABLE


def test_cli():
    """Test the round trip generation of effective settings given some cli parameters."""
    settings = deepcopy(NavigatorConfiguration)
    settings.internals.initializing = True

    params = ["images", "--ll", "debug", "--la", "false"]
    _messages, _exit_messages = parse_and_update(params=params, args=settings)
    # Build the effective settings
    effective = to_effective(settings)

    root = effective["ansible-navigator"]
    assert root["app"] == "images"
    assert root["logging"]["append"] is False
    assert root["logging"]["level"] == "debug"


def test_env(monkeypatch: pytest.MonkeyPatch):
    """Test the round trip generation of effective settings given some environment variables.

    :param monkeypatch: The pytest monkeypatch fixture
    """
    settings = deepcopy(NavigatorConfiguration)
    settings.internals.initializing = True

    prefix = settings.application_name
    monkeypatch.setenv(settings.entry("app").environment_variable(prefix), "images")
    monkeypatch.setenv(settings.entry("log_level").environment_variable(prefix), "debug")
    monkeypatch.setenv(settings.entry("log_append").environment_variable(prefix), "false")

    _messages, _exit_messages = parse_and_update(params=[], args=settings)
    # Build the effective settings
    effective = to_effective(settings)

    root = effective["ansible-navigator"]
    assert isinstance(root, dict)
    assert root["app"] == "images"
    assert root["logging"]["append"] is False
    assert root["logging"]["level"] == "debug"


def test_full(
    settings_env_var_to_full: tuple[Path, SettingsFileType],
):
    """Test the round trip generation of effective settings given a full settings file.

    :param settings_env_var_to_full: The env var and file writing fixture
    """
    sample: dict = settings_env_var_to_full[1]

    settings = deepcopy(NavigatorConfiguration)
    settings.internals.initializing = True
    _messages, _exit_messages = parse_and_update(params=[], args=settings)

    # Build the effective settings
    effective: dict = to_effective(settings)

    # Compare the effective against the settings sample
    type_check_only = [
        "ansible-navigator.ansible.inventory.entries",  # might be paths or not
    ]

    # Walk the settings, for each path extract the value from the sample and effective and compare
    for entry in settings.entries:
        path = entry.settings_file_path(prefix=settings.application_name_dashed)
        effective_value = reduce(operator.getitem, path.split("."), effective)
        sample_value = reduce(operator.getitem, path.split("."), sample)
        # Don't check auto
        if entry.value.source == Constants.AUTO:
            continue
        # Compare, or try to resolve full paths and compare
        try:
            assert effective_value == sample_value
        except AssertionError:
            if path in type_check_only:
                assert isinstance(effective_value, type(sample_value))
            else:
                assert isinstance(effective_value, str)
                assert isinstance(sample_value, str)
                assert abs_user_path(effective_value) == abs_user_path(sample_value)
