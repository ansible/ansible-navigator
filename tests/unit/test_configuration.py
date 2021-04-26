""" tests for configuration subsystem
"""
from collections import Counter

from ansible_navigator.configuration import ApplicationConfiguration
from ansible_navigator.configuration import Configuration

from ansible_navigator.yaml import yaml
from ansible_navigator.yaml import Dumper


def generate_config(params, settings_file_path, save_as_initial=False, apply_previous_cli=False):
    application_configuration = ApplicationConfiguration
    configuration = Configuration(
        application_configuration=application_configuration,
        params=params,
        settings_file_path=settings_file_path,
        save_as_intitial=save_as_initial,
        apply_previous_cli=apply_previous_cli,
    )
    msgs = configuration.configure()
    return msgs, application_configuration


def test_no_dash_in_name():
    """Ensure no names contain a -"""
    for entry in ApplicationConfiguration.entries:
        assert "-" not in entry.name


def test_no_short_long_if_postional():
    """Ensure no postional argument has a short or long set"""
    for entry in ApplicationConfiguration.entries:
        if hasattr(entry, "cli_arguments") and entry.cli_parameters.positional:
            assert entry.short is None
            assert entry.long_override is None


def test_no_underscore_in_path():
    """Ensure no long override has an _"""
    for entry in ApplicationConfiguration.entries:
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


def test_all_entries_set_to_default(tmpdir):
    """Ensure all entries are set to a default value"""
    config = {"ansible-navigator": None}
    settings_file_path = tmpdir.join("ansible-navigator.yaml")
    with open(settings_file_path, "w") as file:
        yaml.dump(config, file, Dumper=Dumper)
    _msgs, application_configuration = generate_config(
        params="", settings_file_path=settings_file_path
    )
    for entry in application_configuration.entries:
        assert entry.value.source.name == "DEFAULT_CFG", entry
        if entry.name not in ["inventory", "pass_environment_variable"]:
            assert entry.value.current == entry.value.default, entry
        else:
            assert entry.value.current == [], entry
