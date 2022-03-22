"""tests for configuration subsystem

Note about decorators:

@patch("shutil.which",return_value="/path/to/container_engine")
- ensure the container engine check in post_process does not fail

@patch("os.path.isfile",return_value=True)
- ensure the playbook_artifact_load file does not fail in post processing

"""
import os
import shlex

# pylint: disable=preferred-module  # FIXME: remove once migrated per GH-872
from unittest import mock
from unittest.mock import patch

import pytest

from ansible_navigator.configuration_subsystem.definitions import Constants as C
from ansible_navigator.configuration_subsystem.navigator_configuration import (
    NavigatorConfiguration,
)
from .data import BASE_EXPECTED
from .data import BASE_LONG_CLI
from .data import BASE_SHORT_CLI
from .data import CLI_DATA
from .data import ENV_VAR_DATA
from .data import SETTINGS
from .utils import config_post_process
from .utils import id_for_base
from .utils import id_for_cli
from .utils import id_for_name
from .utils import id_for_settings


# pylint: disable=too-many-arguments


@pytest.mark.usefixtures("ansible_version")
@patch("shutil.which", return_value="/path/to/container_engine")
@patch("os.path.isfile", return_value=True)
@pytest.mark.parametrize("base", (None, BASE_SHORT_CLI, BASE_LONG_CLI), ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_env_vars(
    _mf1,
    _mf2,
    generate_config,
    base,
    cli_entry,
    expected,
):
    """Ensure all entries are set by the CLI, even with environment variables set."""
    if base is None:
        params = shlex.split(cli_entry)
        expected = dict(expected)
    else:
        cli_entry_split = shlex.split(cli_entry)
        params = cli_entry_split + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    env_vars = {}
    for entry in NavigatorConfiguration.entries:
        env_var_name = entry.environment_variable("ansible_navigator")
        env_var_value = [value[1] for value in ENV_VAR_DATA if value[0] == entry.name]
        assert len(env_var_value) == 1, entry.name
        env_vars[env_var_name] = env_var_value[0]

    with mock.patch.dict(os.environ, env_vars):
        response = generate_config(params=params)
        assert response.exit_messages == []
        for key, value in expected.items():
            assert response.application_configuration.entry(key).value.current == value, key
            assert response.application_configuration.entry(key).value.source is C.USER_CLI, key
        for entry in response.application_configuration.entries:
            if entry.name not in expected:
                assert entry.value.source is C.ENVIRONMENT_VARIABLE, entry.name


@pytest.mark.usefixtures("ansible_version")
@patch("shutil.which", return_value="/path/to/container_engine")
@patch("os.path.isfile", return_value=True)
@pytest.mark.parametrize("settings, settings_file_type", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", (None, BASE_SHORT_CLI, BASE_LONG_CLI), ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_settings(
    _mf1,
    _mf2,
    generate_config,
    settings,
    settings_file_type,
    base,
    cli_entry,
    expected,
):
    """Ensure all entries are set by the CLI
    based on the settings file, the non CLI parameters will be
    either DEFAULT_CFG or USER_CFG
    """
    if base is None:
        params = shlex.split(cli_entry)
        expected = dict(expected)
    else:
        cli_entry_split = shlex.split(cli_entry)
        params = cli_entry_split + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    response = generate_config(params=params, setting_file_name=settings)
    assert response.exit_messages == []
    for entry in response.application_configuration.entries:
        if entry.name in expected:
            assert entry.value.current == expected[entry.name], entry.name
            assert entry.value.source is C.USER_CLI, entry.name
        else:
            if settings_file_type == "empty":
                if entry.value.default is C.NOT_SET:
                    assert entry.value.source is C.NOT_SET, entry.name
                elif entry.value.default == "auto":
                    assert entry.value.source is C.AUTO, entry.name
                else:
                    assert entry.value.source is C.DEFAULT_CFG, entry.name
            elif settings_file_type == "full":
                assert entry.value.source is C.USER_CFG, entry.name


@pytest.mark.usefixtures("ansible_version")
@patch("shutil.which", return_value="/path/to/container_engine")
@patch("os.path.isfile", return_value=True)
@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", (None, BASE_SHORT_CLI, BASE_LONG_CLI), ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_settings_and_env_vars(
    _mf1,
    _mf2,
    generate_config,
    settings,
    source_other,
    base,
    cli_entry,
    expected,
):
    # pylint: disable=unused-argument
    """Ensure all entries are set by the CLI
    the non CLI parameters will be all be ENVIRONMENT_VARIABLE
    even though an empty or full settings file was provided
    """
    if base is None:
        params = shlex.split(cli_entry)
        expected = dict(expected)
    else:
        params = shlex.split(cli_entry) + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    env_vars = {}
    for entry in NavigatorConfiguration.entries:
        env_var_name = entry.environment_variable("ansible_navigator")
        env_var_value = [value[1] for value in ENV_VAR_DATA if value[0] == entry.name]
        assert len(env_var_value) == 1, entry.name
        env_vars[env_var_name] = env_var_value[0]

    with mock.patch.dict(os.environ, env_vars):
        response = generate_config(params=params, setting_file_name=settings)
        assert response.exit_messages == []
        for key, value in expected.items():
            configured_entry = response.application_configuration.entry(key)
            assert configured_entry.value.current == value, configured_entry.name
            assert configured_entry.value.source is C.USER_CLI, configured_entry.name
        for entry in response.application_configuration.entries:
            if entry.name not in expected:
                assert entry.value.source is C.ENVIRONMENT_VARIABLE, entry.name


@pytest.mark.usefixtures("ansible_version")
@patch("shutil.which", return_value="/path/to/container_engine")
@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_default(_mocked_func, generate_config, entry):
    """Ensure all entries are set to a default value"""
    response = generate_config()
    assert response.exit_messages == []
    configured_entry = response.application_configuration.entry(entry.name)
    if configured_entry.value.default is C.NOT_SET:
        assert configured_entry.value.source is C.NOT_SET, configured_entry
    else:
        if configured_entry.name == "playbook_save_as":
            assert configured_entry.value.source is C.DEFAULT_CFG, configured_entry
            assert configured_entry.value.current.endswith(entry.value.default), configured_entry
        elif configured_entry.name == "container_engine":
            assert configured_entry.value.source is C.AUTO, configured_entry
            assert configured_entry.value.current == "podman"
        else:
            assert configured_entry.value.source is C.DEFAULT_CFG, configured_entry
            assert configured_entry.value.current == entry.value.default, configured_entry


@pytest.mark.usefixtures("ansible_version")
@patch("shutil.which", return_value="/path/to/container_engine")
@patch("os.path.isfile", return_value=True)
@pytest.mark.parametrize("settings, settings_file_type", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("entry, value, expected", ENV_VAR_DATA)
def test_all_entries_reflect_env_var_given_settings(
    _mf1,
    _mf2,
    generate_config,
    settings,
    settings_file_type,
    entry,
    value,
    expected,
):
    """Ensure each entry is are set by an environment variables
    even though settings file has been provided, the others
    should by default or settings file
    """
    environment_variable = NavigatorConfiguration.entry(entry).environment_variable(
        "ansible_navigator",
    )
    with mock.patch.dict(os.environ, {environment_variable: str(value)}):
        response = generate_config(setting_file_name=settings)
        assert response.exit_messages == []
        configured_entry = response.application_configuration.entry(entry)
    assert configured_entry.value.source is C.ENVIRONMENT_VARIABLE
    assert configured_entry.value.current == expected

    for other_entry in response.application_configuration.entries:
        if other_entry.name != entry:
            if settings_file_type == "empty":
                if other_entry.value.default is C.NOT_SET:
                    assert other_entry.value.source is C.NOT_SET, entry.name
                elif other_entry.value.default == "auto":
                    assert other_entry.value.source is C.AUTO, entry.name
                else:
                    assert other_entry.value.source is C.DEFAULT_CFG, entry.name
            elif settings_file_type == "full":
                assert other_entry.value.source is C.USER_CFG, entry.name


@pytest.mark.usefixtures("ansible_version")
@patch("shutil.which", return_value="/path/to/container_engine")
@patch("os.path.isfile", return_value=True)
@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_settings_given_settings(_mf1, _mf2, generate_config, entry):
    """Ensure all entries are set to an entry in a settings file"""
    response = generate_config(setting_file_name="ansible-navigator.yml")
    assert response.exit_messages == []
    configured_entry = response.application_configuration.entry(entry.name)
    if entry.cli_parameters is not None:
        assert configured_entry.value.source is C.USER_CFG, configured_entry
        path = entry.settings_file_path("ansible-navigator")
        expected = config_post_process(response.settings_contents, path)

        for key in path.split("."):
            expected = expected[key]
        assert configured_entry.value.current == expected, configured_entry
