"""Some sanity and syntax checking of the navigator configuration."""
from collections import Counter
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem.definitions import Constants as C
from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.navigator_configuration import SettingsEntry

from .utils import id_for_name


def test_entries_no_duplicate_names():
    """Ensure no name is duplicated."""
    values = Counter([entry.name for entry in NavigatorConfiguration.entries])
    assert not any(k for (k, v) in values.items() if v > 1)


def test_entries_no_duplicate_shorts():
    """Ensure no short is duplicated."""
    values = Counter(
        [
            entry.cli_parameters.short
            for entry in NavigatorConfiguration.entries
            if entry.cli_parameters is not None
        ],
    )
    assert not any(k for (k, v) in values.items() if v > 1)


def test_entries_alphabetical():
    """Ensure entries are alphabetical."""
    values = [entry.name for entry in NavigatorConfiguration.entries]
    assert values == sorted(values)


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_entries_no_dash_in_name(entry: SettingsEntry):
    """Ensure no names contain a -.

    :param entry: The entry to test
    """
    assert "-" not in entry.name


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_entries_no_dash_in_environment_variable(entry: SettingsEntry):
    """Ensure no environment variable has a dash.

    :param entry: The entry to test
    """
    assert "-" not in entry.environment_variable("ansible_navigator")


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_entries_no_short_long_if_positional(entry: SettingsEntry):
    """Ensure no positional argument has a short or long set.

    :param entry: The entry to test
    """
    if (
        hasattr(entry, "cli_arguments")
        and entry.cli_parameters is not None
        and entry.cli_parameters.positional
    ):
        assert entry.cli_parameters.short is None
        assert entry.cli_parameters.long_override is None


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_entries_no_underscore_in_path(entry: SettingsEntry):
    """Ensure no long override has an _.

    :param entry: The entry to test
    """
    if entry.settings_file_path_override is not None:
        assert "_" not in entry.settings_file_path_override


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_entries_no_current_set(entry: SettingsEntry):
    """Ensure no entry has a current value set prior to configuration.

    :param entry: The entry to test
    """
    assert entry.value.current is C.NOT_SET


@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_entries_default_value(entry: SettingsEntry):
    """Ensure entry has a default value not set or a common type.

    :param entry: The entry to test
    """
    if isinstance(entry.value.default, C):
        assert entry.value.default is C.NOT_SET
    else:
        assert isinstance(entry.value.default, (bool, int, str, dict, list, Path))
