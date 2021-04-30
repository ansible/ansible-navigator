""" tests for configuration subsystem
"""
import os

from unittest import mock

import pytest

from ansible_navigator.configuration_subsystem.configurator import Configurator

from ansible_navigator.configuration_subsystem.definitions import Constants as C

from ansible_navigator.configuration_subsystem.navigator_configuration import (
    generate_editor_command,
)
from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration


from .data import BASE_EXPECTED
from .data import BASE_LONG_CLI
from .data import BASE_SHORT_CLI
from .data import CLI_DATA
from .data import ENVVAR_DATA
from .data import SETTINGS

from .utils import fixture_generate_config  # pylint: disable=unused-import
from .utils import id_for_base
from .utils import id_for_cli
from .utils import id_for_name
from .utils import id_for_settings


# pylint: disable=too-many-arguments


def test_data_no_missing_envvar_data():
    """Ensure the ENVVAR_DATA covers all entries"""
    entry_names = [entry.name for entry in NavigatorConfiguration.entries]
    data_names = [entry[0] for entry in ENVVAR_DATA]
    assert entry_names == data_names


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_default(generate_config, entry):
    """Ensure all entries are set to a default value"""
    response = generate_config()
    configured_entry = response.application_configuration.entry(entry.name)
    if configured_entry.value.default is C.NOT_SET:
        assert configured_entry.value.source is C.NOT_SET, entry
    else:
        assert configured_entry.value.source is C.DEFAULT_CFG, entry
        assert configured_entry.value.current == entry.value.default, entry


@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_envvars(generate_config, base, cli_entry, expected):
    """Ensure all entries are set by the cli even with envvars set"""
    if base is None:
        params = cli_entry.split()
        expected = dict(expected)
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    envvars = {}
    for entry in NavigatorConfiguration.entries:
        envvar_name = entry.environment_variable("ansible_navigator")
        envvar_value = [value[1] for value in ENVVAR_DATA if value[0] == entry.name]
        assert len(envvar_value) == 1, entry.name
        envvars[envvar_name] = envvar_value[0]

    with mock.patch.dict(os.environ, envvars):
        response = generate_config(params=params)
        for key, value in expected.items():
            assert response.application_configuration.entry(key).value.current == value
            assert response.application_configuration.entry(key).value.source is C.USER_CLI
        for entry in response.application_configuration.entries:
            if entry.name not in expected:
                assert entry.value.source is C.ENVIRONMENT_VARIABLE, entry


@pytest.mark.parametrize("settings, settings_file_type", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_settings(
    generate_config, settings, settings_file_type, base, cli_entry, expected
):
    """Ensure all entries are set by the cli
    based on the settings file, the non cli parametes will be
    either DEFAULT_CFG or USER_CFG
    """
    if base is None:
        params = cli_entry.split()
        expected = dict(expected)
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    response = generate_config(params=params, setting_file_name=settings)

    for entry in response.application_configuration.entries:
        if entry.name in expected:
            assert entry.value.current == expected[entry.name], entry
            assert entry.value.source is C.USER_CLI, entry
        else:
            if settings_file_type == "empty":
                if entry.value.default is C.NOT_SET:
                    assert entry.value.source is C.NOT_SET, entry
                else:
                    assert entry.value.source is C.DEFAULT_CFG, entry
            elif settings_file_type == "full":
                assert entry.value.source is C.USER_CFG, entry


@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli_given_settings_and_envars(
    generate_config, settings, source_other, base, cli_entry, expected
):
    # pylint: disable=unused-argument
    """Ensure all entries are set by the cli
    the non cli parametes will be all be ENVIRONMENT_VARIABLE
    even though an empty or full settings file was provided
    """
    if base is None:
        params = cli_entry.split()
        expected = dict(expected)
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected = {**dict(expected), **dict(BASE_EXPECTED)}

    envvars = {}
    for entry in NavigatorConfiguration.entries:
        envvar_name = entry.environment_variable("ansible_navigator")
        envvar_value = [value[1] for value in ENVVAR_DATA if value[0] == entry.name]
        assert len(envvar_value) == 1, entry.name
        envvars[envvar_name] = envvar_value[0]

    with mock.patch.dict(os.environ, envvars):
        response = generate_config(params=params, setting_file_name=settings)
        for key, value in expected.items():
            configured_entry = response.application_configuration.entry(key)
            assert configured_entry.value.current == value, configured_entry
            assert configured_entry.value.source is C.USER_CLI, configured_entry
        for entry in response.application_configuration.entries:
            if entry.name not in expected:
                assert entry.value.source is C.ENVIRONMENT_VARIABLE, entry


@pytest.mark.parametrize("settings, settings_file_type", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("entry, value, expected", ENVVAR_DATA)
def test_all_entries_reflect_envvar_given_settings(
    generate_config, settings, settings_file_type, entry, value, expected
):
    # pylint: disable=unused-argument
    """Ensure each entry is are set by an environment variables
    even though settings file has been provided, the others
    should by default or user cfg
    """
    environment_variable = NavigatorConfiguration.entry(entry).environment_variable(
        "ansible_navigator"
    )
    with mock.patch.dict(os.environ, {environment_variable: str(value)}):
        response = generate_config(setting_file_name=settings)
        configured_entry = response.application_configuration.entry(entry)
    assert configured_entry.value.source is C.ENVIRONMENT_VARIABLE
    assert configured_entry.value.current == expected

    for other_entry in response.application_configuration.entries:
        if other_entry.name != entry:
            if settings_file_type == "empty":
                if other_entry.value.default is C.NOT_SET:
                    assert other_entry.value.source is C.NOT_SET, entry
                else:
                    assert other_entry.value.source is C.DEFAULT_CFG, entry
            elif settings_file_type == "full":
                assert other_entry.value.source is C.USER_CFG, entry


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_settings_given_settings(generate_config, entry):
    """Ensure all entries are set to an entry in a settings file"""
    response = generate_config(setting_file_name="ansible-navigator.yml")
    configured_entry = response.application_configuration.entry(entry.name)
    if entry.cli_parameters is not None:
        assert configured_entry.value.source is C.USER_CFG, entry
        path = entry.settings_file_path("ansible-navigator")
        expected = response.settings_contents
        for key in path.split("."):
            expected = expected[key]
        assert configured_entry.value.current == expected, entry


def test_editor_command_from_editor(generate_config):
    """Ensure the editor_command defaults to EDITOR if set"""
    with mock.patch.dict(os.environ, {"EDITOR": "nano"}):
        # since this was already loaded, force it
        NavigatorConfiguration.entry("editor_command").value.default = generate_editor_command()
        response = generate_config()
        assert response.application_configuration.editor_command == "nano {filename}"


def test_not_a_bool(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for wrong type of value"""

    response = generate_config(setting_file_name="ansible-navigator_not_bool.yml")
    errors = [
        (
            "execution-environment must be one of 'True' or 'False',"
            " but set as '5' in user provided configuration file"
        )
    ]
    assert response.errors == errors


def test_badly_formatted_envar(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for badly formatted set env var"""
    params = "run site.yml --senv TK1:TV1"
    response = generate_config(params=params.split())
    errors = ["The following set-environment-variable entry could not be parsed: TK1:TV1"]
    assert response.errors == errors


def test_broken_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for broken settings file"""
    response = generate_config(setting_file_name="ansible-navigator_broken.yml")
    assert len(response.errors) == 1
    error = "/ansible-navigator_broken.yml empty"
    assert response.errors[0].endswith(error)


def test_garbage_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for garbage settings file"""
    response = generate_config(setting_file_name=os.path.abspath(__file__))
    assert len(response.errors) == 1
    error = "but failed to load it."
    assert response.errors[0].endswith(error)


def test_inventory_no_inventory(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for an inventory without an inventory specified"""
    response = generate_config(params=["inventory"])
    errors = ["An inventory is required when using the inventory subcommand"]
    assert response.errors == errors


def test_mutual_exclusivity_for_configuration_init():
    """Ensure the configuration cannot be intited with both
    apply_previous_cli_entries and save_as_intitial"""
    with pytest.raises(ValueError, match="cannot be used with"):
        Configurator(
            params=None,
            application_configuration=None,
            save_as_intitial=True,
            apply_previous_cli_entries=C.ALL,
        )


def test_apply_before_initial_saved():
    """Ensure the apply_previous_cli_entries cant' be used before save_as_intitial"""
    with pytest.raises(ValueError, match="enabled prior to"):
        Configurator(
            params=None,
            application_configuration=NavigatorConfiguration,
            apply_previous_cli_entries=C.ALL,
        ).configure()


@pytest.mark.parametrize(
    "entry", [entry for entry in NavigatorConfiguration.entries if entry.choices], ids=id_for_name
)
def test_poor_choices(generate_config, entry):
    # pylint: disable=import-outside-toplevel
    """Ensure errors generated for poor choices"""

    def test(param):
        response = generate_config(params=[param, "Sentinel"])
        assert len(response.errors) == 1
        error = "must be one"
        assert error in response.errors[0]

    test(entry.cli_parameters.short)
    test(entry.cli_parameters.long_override or f"--{entry.name_dashed}")


def test_generate_argparse_error(generate_config):
    """Ensure errors generated by argparse are caught"""
    params = "Sentinel"
    response = generate_config(params=params.split())
    assert len(response.errors) == 1
    error = "invalid choice: 'Sentinel'"
    assert error in response.errors[0]
