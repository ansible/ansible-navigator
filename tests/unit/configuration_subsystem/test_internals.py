"""Test the internals of a NavigatorConfiguration."""

from copy import deepcopy
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.initialization import parse_and_update

from .defaults import TEST_FIXTURE_DIR


def test_settings_file_path_file_none() -> None:
    """Confirm a settings file path is not stored in the internals when not present."""
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    parse_and_update(params=[], args=args)
    assert args.internals.settings_file_path is None
    assert args.internals.settings_source == Constants.NONE


def test_settings_file_path_file_system(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm a settings file path is stored in the internals when searched.

    Args:
        monkeypatch: Fixture providing these helper methods for safely
            patching and mocking functionality in tests
    """
    settings_file = "ansible-navigator.yml"
    settings_file_path = TEST_FIXTURE_DIR / settings_file
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    args.application_version = "test"

    def getcwd() -> Path:
        return TEST_FIXTURE_DIR

    monkeypatch.setattr(Path, "cwd", getcwd)
    parse_and_update(params=[], args=args)
    assert args.internals.settings_file_path == str(settings_file_path)
    assert args.internals.settings_source == Constants.SEARCH_PATH


def test_settings_file_path_environment_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm a settings file path is stored in the internals when set via environment variable.

    Args:
        monkeypatch: Fixture providing these helper methods for safely
            patching and mocking functionality in tests
    """
    settings_file = "ansible-navigator.yml"
    settings_file_path = TEST_FIXTURE_DIR / settings_file
    monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", str(settings_file_path))
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    args.application_version = "test"
    parse_and_update(params=[], args=args)
    assert args.internals.settings_file_path == str(settings_file_path)
    assert args.internals.settings_source == Constants.ENVIRONMENT_VARIABLE
