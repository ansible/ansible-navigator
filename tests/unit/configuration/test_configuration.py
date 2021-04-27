""" tests for configuration subsystem
"""
import os
from collections import Counter
from copy import deepcopy
from unittest import mock

import pytest

from ansible_navigator.configuration.application_configuration import generate_editor_command
from ansible_navigator.configuration import ApplicationConfiguration
from ansible_navigator.configuration import Configuration
from ansible_navigator.configuration.definitions import Config


from .data import BASE_EXPECTED
from .data import BASE_LONG_CLI
from .data import BASE_SHORT_CLI
from .data import CLI_DATA
from .data import ENVVAR_DATA
from .data import SETTINGS

from .utils import fixture_generate_config
from .utils import generate_params_from_entries
from .utils import id_for_base
from .utils import id_for_cli
from .utils import id_for_name
from .utils import id_for_settings

from ...defaults import FIXTURES_DIR


def pytest_generate_tests(metafunc):
    """Parameterize tests calling for a specific fixture"""
    if "empty" in metafunc.fixturenames:
        argvalues, ids = generate_params_from_entries("ansible-navigator_empty.yml")
        metafunc.parametrize("empty", argvalues, ids=ids)
    elif "full" in metafunc.fixturenames:
        argvalues, ids = generate_params_from_entries("ansible-navigator.yml")
        metafunc.parametrize("full", argvalues, ids=ids)


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=id_for_name)
def test_no_dash_in_name(entry):
    """Ensure no names contain a -"""
    assert "-" not in entry.name


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=id_for_name)
def test_no_dash_in_environment_variable(entry):
    """Ensure no environment variable has a dash"""
    assert "-" not in entry.environment_variable("ansible_navigator")


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=id_for_name)
def test_no_short_long_if_postional(entry):
    """Ensure no postional argument has a short or long set"""
    if hasattr(entry, "cli_arguments") and entry.cli_parameters.positional:
        assert entry.short is None
        assert entry.long_override is None


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=id_for_name)
def test_no_underscore_in_path(entry):
    """Ensure no long override has an _"""
    if entry.settings_file_path_override is not None:
        assert "_" not in entry.settings_file_path_override


def test_no_duplicate_names():
    """Ensure no name is duplicated"""
    values = Counter([entry.name for entry in ApplicationConfiguration.entries])
    assert not any(k for (k, v) in values.items() if v > 1)


def test_no_duplicate_shorts():
    """Ensure no short is duplicated"""
    values = Counter(
        [
            entry.cli_parameters.short
            for entry in ApplicationConfiguration.entries
            if entry.cli_parameters is not None
        ]
    )
    assert not any(k for (k, v) in values.items() if v > 1)


def test_entries_are_alphbetical():
    """Ensure entries are alphabetical"""
    values = [entry.name for entry in ApplicationConfiguration.entries]
    assert values == sorted(values)


def test_all_entries_set_to_default(empty):
    """Ensure all entries are set to a default value"""
    entry, _expected = empty
    assert entry.value.source.name == "DEFAULT_CFG", entry
    if entry.name not in ["inventory", "inventory_column", "pass_environment_variable"]:
        assert entry.value.current == entry.value.default, entry
    else:
        assert entry.value.current == [], entry


def test_all_entries_reflect_settings_file(full):
    """Ensure all entries are set to an entry in a settings file"""
    entry, expected = full
    if entry.cli_parameters is not None:
        assert entry.value.source.name == "USER_CFG", entry
        path = entry.settings_file_path("ansible-navigator")
        for key in path.split("."):
            expected = expected[key]
        assert entry.value.current == expected, entry


def test_no_missing_envvar_data():
    """Ensure the ENVVAR_DATA covers all entries"""
    entry_names = [entry.name for entry in ApplicationConfiguration.entries]
    data_names = [entry[0] for entry in ENVVAR_DATA]
    assert entry_names == data_names


@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("entry, value, expected", ENVVAR_DATA)
def test_all_entries_reflect_envar_settings(
    generate_config, settings, source_other, entry, value, expected
):
    # pylint: disable=unused-argument
    """Ensure all entries are set to an entry in a settings file"""
    environment_variable = ApplicationConfiguration.entry(entry).environment_variable(
        "ansible_navigator"
    )
    with mock.patch.dict(os.environ, {environment_variable: str(value)}):
        application_configuration, _settings_contents = generate_config(setting_file_name=settings)
        entry = application_configuration.entry(entry)
        assert entry.value.source.name == "ENVIRONMENT_VARIABLE"
        assert entry.value.current == expected


@pytest.mark.parametrize("settings, source_other", SETTINGS, ids=id_for_settings)
@pytest.mark.parametrize("base", [None, BASE_SHORT_CLI, BASE_LONG_CLI], ids=id_for_base)
@pytest.mark.parametrize("cli_entry, expected", CLI_DATA, ids=id_for_cli)
def test_all_entries_reflect_cli(
    generate_config, settings, source_other, base, cli_entry, expected
):
    """Ensure all entries are set by the cli"""
    if base is None:
        params = cli_entry.split()
    else:
        params = cli_entry.split() + " ".join(base.splitlines()).split()
        expected.update(BASE_EXPECTED)
    application_configuration, _settings_contents = generate_config(
        params=params, setting_file_name=settings
    )
    for key, value in expected.items():
        assert application_configuration.entry(key).value.current == value
        assert application_configuration.entry(key).value.source.name == "USER_CLI"
    for entry in application_configuration.entries:
        if entry.name not in expected:
            assert entry.value.source.name == source_other, entry


def test_apply_previous_cli(generate_config):
    params = "doc shell --ee False --eei test_image"
    expected = {
        "app": "doc",
        "execution_environment": False,
        "execution_environment_image": "test_image",
    }

    application_configuration = deepcopy(ApplicationConfiguration)
    configuration = Configuration(
        application_configuration=application_configuration,
        params=params.split(),
        save_as_intitial=True,
    )
    configuration.configure()
    for key, value in expected.items():
        assert application_configuration.entry(key).value.current == value
        assert application_configuration.entry(key).value.source.name == "USER_CLI"

    assert isinstance(application_configuration.initial, Config)

    params = "doc"
    configuration = Configuration(
        application_configuration=application_configuration,
        params=params.split(),
        apply_previous_cli=True,
    )
    configuration.configure()
    for key, value in expected.items():
        if key != "app":
            assert application_configuration.entry(key).value.current == value
            assert application_configuration.entry(key).value.source.name == "PREVIOUS_CLI"


def test_editor_command_from_editor(generate_config):
    """Ensure the editor_command defaults to EDITOR if set"""
    with mock.patch.dict(os.environ, {"EDITOR": "nano"}):
        # since this was already loaded, force it
        ApplicationConfiguration.entry("editor_command").value.default = generate_editor_command()
        application_configuration, _settings_contents = generate_config()
        assert application_configuration.editor_command == "nano {filename}"


def test_not_a_bool(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure exit early for wrong type of value"""
    import ansible_navigator.configuration.configuration

    with mock.patch.object(
        ansible_navigator.configuration.configuration, "error_and_exit_early"
    ) as mock_method:
        mock_method.side_effect = Exception("called")
        with pytest.raises(Exception, match="called"):
            _application_configuration, _settings_contents = generate_config(
                setting_file_name="ansible-navigator_not_bool.yml"
            )
    _args, kwargs = mock_method.call_args
    assert len(kwargs["errors"]) == 1
    error = (
        "execution-environment must be one of 'True' or 'False',"
        " but set as '5' in user provided configuration file"
    )
    assert kwargs["errors"][0] == error


def test_badly_formatted_envar(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure exit early for badly formatted set env var"""
    import ansible_navigator.configuration.configuration

    params = "run site.yml --senv TK1:TV1"
    with mock.patch.object(
        ansible_navigator.configuration.configuration, "error_and_exit_early"
    ) as mock_method:
        mock_method.side_effect = Exception("called")
        with pytest.raises(Exception, match="called"):
            _application_configuration, _settings_contents = generate_config(params=params.split())
    _args, kwargs = mock_method.call_args
    assert len(kwargs["errors"]) == 1
    error = "The following set-environment-variable entry could not be parsed: TK1:TV1"
    assert kwargs["errors"][0] == error


def test_broken_settings_file(generate_config):
    # pylint: disable=import-outside-toplevel
    """Ensure exit early for wrong type of value"""
    import ansible_navigator.configuration.configuration

    with mock.patch.object(
        ansible_navigator.configuration.configuration, "error_and_exit_early"
    ) as mock_method:
        mock_method.side_effect = Exception("called")
        with pytest.raises(Exception, match="called"):
            _application_configuration, _settings_contents = generate_config(
                setting_file_name="ansible-navigator_broken.yml"
            )
    _args, kwargs = mock_method.call_args
    assert len(kwargs["errors"]) == 1
    error = "/ansible-navigator_broken.yml empty"
    assert kwargs["errors"][0].endswith(error)
