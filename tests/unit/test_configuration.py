""" tests for configuration subsystem
"""
import os
import sys
from collections import Counter
from copy import deepcopy
from unittest import mock


import pytest

from ansible_navigator.configuration.application_configuration import generate_editor_command
from ansible_navigator.configuration import ApplicationConfiguration
from ansible_navigator.configuration import Configuration

from ansible_navigator.configuration.definitions import Entry

from ansible_navigator.yaml import yaml
from ansible_navigator.yaml import Loader

from ..defaults import FIXTURES_DIR

TEST_FIXTURE_DIR = os.path.join(FIXTURES_DIR, "unit", "configuration")


def name_for_id(val):
    """Return an id based on entry name"""
    if isinstance(val, Entry):
        return val.name
    return ""


def generate_config(setting_file_name=None):
    """Generate a configuration given a settings file"""
    if setting_file_name:
        settings_file_path = os.path.join(TEST_FIXTURE_DIR, setting_file_name)
        with open(settings_file_path) as file:
            settings_contents = yaml.load(file, Loader=Loader)
    else:
        settings_file_path = None
        settings_contents = {}

    application_configuration = deepcopy(ApplicationConfiguration)
    configuration = Configuration(
        application_configuration=application_configuration,
        params="",
        settings_file_path=settings_file_path,
    )
    configuration.configure()
    return application_configuration, settings_contents


def generate_params_from_entries(setting_file_name):
    """Generate params from a configurations' entries"""
    application_configuration, settings_contents = generate_config(setting_file_name)
    argvalues = [(entry, settings_contents) for entry in application_configuration.entries]
    ids = [entry.name for entry in application_configuration.entries]
    return argvalues, ids


def pytest_generate_tests(metafunc):
    """Parameterize tests calling for a specific fixture"""
    if "empty" in metafunc.fixturenames:
        argvalues, ids = generate_params_from_entries("ansible-navigator_empty.yml")
        metafunc.parametrize("empty", argvalues, ids=ids)
    elif "full" in metafunc.fixturenames:
        argvalues, ids = generate_params_from_entries("ansible-navigator.yml")
        metafunc.parametrize("full", argvalues, ids=ids)


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=name_for_id)
def test_no_dash_in_name(entry):
    """Ensure no names contain a -"""
    assert "-" not in entry.name


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=name_for_id)
def test_no_dash_in_environment_variable(entry):
    """Ensure no environment variable has a dash"""
    assert "-" not in entry.environment_variable("ansible_navigator")


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=name_for_id)
def test_no_short_long_if_postional(entry):
    """Ensure no postional argument has a short or long set"""
    if hasattr(entry, "cli_arguments") and entry.cli_parameters.positional:
        assert entry.short is None
        assert entry.long_override is None


@pytest.mark.parametrize("entry", ApplicationConfiguration.entries, ids=name_for_id)
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
    if entry.name not in ["inventory", "pass_environment_variable"]:
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


test_data = [
    ("app", "doc", "doc"),
    ("cmdline", "--forks 15", ["--forks", "15"]),
    ("container_engine", "docker", "docker"),
    ("editor_command", "nano", "nano"),
    ("editor_console", "false", False),
    ("execution_environment", "false", False),
    ("execution_environment_image", "test_image", "test_image"),
    ("inventory", "/tmp/test1.yaml,/tmp/test2.yml", ["/tmp/test1.yaml", "/tmp/test2.yml"]),
    ("inventory_column", "t1,t2,t3", ["t1", "t2", "t3"]),
    ("log_file", "/tmp/app.log", "/tmp/app.log"),
    ("log_level", "info", "info"),
    ("mode", "stdout", "stdout"),
    ("osc4", "false", False),
    ("pass_environment_variable", "a,b,c", ["a", "b", "c"]),
    ("playbook", "/tmp/site.yaml", "/tmp/site.yaml"),
    ("playbook_artifact", "/tmp/play.json", "/tmp/play.json"),
    ("plugin_name", "shell", "shell"),
    ("plugin_type", "become", "become"),
    ("set_environment_variable", "T1=A,T2=B,T3=C", {"T1": "A", "T2": "B", "T3": "C"}),
]


def test_no_missing_test_data():
    """Ensure the test_data covers all entries"""
    entry_names = [entry.name for entry in ApplicationConfiguration.entries]
    data_names = [entry[0] for entry in test_data]
    assert entry_names == data_names


@pytest.mark.parametrize("entry, value, expected", test_data)
def test_all_entries_reflect_envar_settings(entry, value, expected):
    """Ensure all entries are set to an entry in a settings file"""
    environment_variable = ApplicationConfiguration.entry(entry).environment_variable(
        "ansible_navigator"
    )
    with mock.patch.dict(os.environ, {environment_variable: str(value)}):
        application_configuration, _settings_contents = generate_config("ansible-navigator.yml")
        entry = application_configuration.entry(entry)
        assert entry.value.source.name == "ENVIRONMENT_VARIABLE"
        assert entry.value.current == expected


def test_editor_command_from_editor():
    """Ensure the editor_command defaults to EDITOR if set"""
    with mock.patch.dict(os.environ, {"EDITOR": "nano"}):
        # since this was already loaded, force it
        ApplicationConfiguration.entry("editor_command").value.default = generate_editor_command()
        application_configuration, _settings_contents = generate_config()
        assert application_configuration.editor_command == "nano {filename}"


def test_not_a_bool():
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
