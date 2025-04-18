"""Tests for configuration subsystem."""

from __future__ import annotations

import pathlib
import shlex

from typing import TYPE_CHECKING
from typing import Any

import pytest

from ansible_navigator.configuration_subsystem.definitions import Constants as C
from ansible_navigator.configuration_subsystem.definitions import SettingsEntry
from ansible_navigator.configuration_subsystem.navigator_configuration import NavigatorConfiguration

from .data import BASE_EXPECTED
from .data import BASE_LONG_CLI
from .data import BASE_SHORT_CLI
from .data import CLI_DATA
from .data import ENV_VAR_DATA
from .data import SETTINGS
from .utils import config_post_process
from .utils import id_for_base
from .utils import id_for_name


if TYPE_CHECKING:
    from collections.abc import Iterable

    from .conftest import GenerateConfigCallable

# pylint: disable=too-many-arguments


def which(*_args: Any, **_kwargs: dict[str, Any]) -> str:
    """Return the path to the container engine.

    Args:
        *_args: args
        **_kwargs: kwargs

    Returns:
        path to container engine
    """
    return "/path/to/container_engine"


def isfile(*_args: Any, **_kwargs: dict[str, Any]) -> bool:
    """Return True.

    Args:
        *_args: args
        **_kwargs: kwargs

    Returns:
        True
    """
    return True


@pytest.mark.usefixtures("_ansible_version")
@pytest.mark.parametrize("base", (None, BASE_SHORT_CLI, BASE_LONG_CLI), ids=id_for_base)
@pytest.mark.parametrize(("cli_entry", "expected"), CLI_DATA)
def test_all_entries_reflect_cli_given_env_vars(
    monkeypatch: pytest.MonkeyPatch,
    generate_config: GenerateConfigCallable,
    base: str | None,
    cli_entry: str,
    expected: Iterable[tuple[str, str]],
) -> None:
    # pylint: disable=too-many-locals
    """Ensure all entries are set by the CLI, even with environment variables set.

    Args:
        monkeypatch: Pytest monkeypatch fixture
        generate_config: Fixture for generating a config
        base: CLI parameters or None
        cli_entry: CLI entry
        expected: Expected value

    Raises:
       pytest.fail: If the pytest fails
    """
    monkeypatch.setattr("shutil.which", which)
    monkeypatch.setattr(pathlib.Path, "is_file", isfile)

    expected_dict: dict[str, str]
    if base is None:
        params = shlex.split(cli_entry)
        expected_dict = dict(expected)
    else:
        cli_entry_split = shlex.split(cli_entry)
        params = cli_entry_split + " ".join(base.splitlines()).split()
        expected_dict = {**dict(expected), **dict(BASE_EXPECTED)}

    env_vars = {}
    for entry in NavigatorConfiguration.entries:
        env_var_name = entry.environment_variable("ansible_navigator")
        env_var_value = [value.values[1] for value in ENV_VAR_DATA if value.values[0] == entry.name]
        assert len(env_var_value) == 1, entry.name
        env_vars[env_var_name] = env_var_value[0]

    for env_var, env_value in env_vars.items():
        if not isinstance(env_value, str):
            msg = "Unexpected data"
            raise pytest.fail(msg)
        monkeypatch.setenv(env_var, env_value)

    response = generate_config(params=params)
    assert response.exit_messages == []
    for key, value in expected_dict.items():
        assert response.application_configuration.entry(key).value.current == value, key
        assert response.application_configuration.entry(key).value.source is C.USER_CLI, key
    for entry in response.application_configuration.entries:
        if entry.name not in expected_dict:
            assert entry.value.source is C.ENVIRONMENT_VARIABLE, entry.name


@pytest.mark.usefixtures("_ansible_version")
@pytest.mark.parametrize(("settings", "settings_file_type"), SETTINGS)
@pytest.mark.parametrize("base", (None, BASE_SHORT_CLI, BASE_LONG_CLI), ids=id_for_base)
@pytest.mark.parametrize(("cli_entry", "expected"), CLI_DATA)
def test_all_entries_reflect_cli_given_settings(
    monkeypatch: pytest.MonkeyPatch,
    generate_config: GenerateConfigCallable,
    settings: str,
    settings_file_type: str,
    base: str | None,
    cli_entry: str,
    expected: Iterable[tuple[str, str]],
) -> None:
    """Ensure all entries are set by the CLI.

    Based on the settings file, the non CLI parameters will be
    either DEFAULT_CFG or USER_CFG

    Args:
        monkeypatch: Pytest monkeypatch fixture
        generate_config: Fixture for generating a config
        settings: Settings file name
        settings_file_type: Settings file type
        base: CLI parameters or None
        cli_entry: CLI entry
        expected: Expected value
    """
    monkeypatch.setattr("shutil.which", which)
    monkeypatch.setattr("os.path.isfile", isfile)

    expected_dict: dict[str, str]
    if base is None:
        params = shlex.split(cli_entry)
        expected_dict = dict(expected)
    else:
        cli_entry_split = shlex.split(cli_entry)
        params = cli_entry_split + " ".join(base.splitlines()).split()
        expected_dict = {**dict(expected), **dict(BASE_EXPECTED)}

    response = generate_config(params=params, settings_file_name=settings)
    assert response.exit_messages == []
    for entry in response.application_configuration.entries:
        if entry.name in expected_dict:
            assert entry.value.current == expected_dict[entry.name], entry.name
            assert entry.value.source is C.USER_CLI, entry.name
        elif settings_file_type == "empty":
            if entry.value.default is C.NOT_SET:
                assert entry.value.source is C.NOT_SET, entry.name
            elif entry.value.default == "auto":
                assert entry.value.source is C.AUTO, entry.name
            else:
                assert entry.value.source is C.DEFAULT_CFG, entry.name
        elif settings_file_type == "full":
            assert entry.value.source is C.USER_CFG, entry.name


@pytest.mark.usefixtures("_ansible_version")
@pytest.mark.parametrize(("settings", "source_other"), SETTINGS)
@pytest.mark.parametrize("base", (None, BASE_SHORT_CLI, BASE_LONG_CLI), ids=id_for_base)
@pytest.mark.parametrize(("cli_entry", "expected"), CLI_DATA)
def test_all_entries_reflect_cli_given_settings_and_env_vars(
    monkeypatch: pytest.MonkeyPatch,
    generate_config: GenerateConfigCallable,
    settings: str,
    source_other: str,
    base: str | None,
    cli_entry: str,
    expected: Iterable[tuple[str, str]],
) -> None:
    # pylint:disable=too-many-locals
    """Ensure all entries are set by the CLI.

    The non CLI parameters will be all be ENVIRONMENT_VARIABLE
    even though an empty or full settings file was provided

    Args:
        monkeypatch: Pytest monkeypatch fixture
        generate_config: Fixture for generating a config
        settings: Settings file name
        source_other: Settings file type
        base: CLI parameters or None
        cli_entry: CLI entry
        expected: Expected value

    Raises:
       pytest.fail: If the pytest fails
    """
    monkeypatch.setattr("shutil.which", which)
    monkeypatch.setattr("os.path.isfile", isfile)

    expected_dict: dict[str, str]
    if base is None:
        params = shlex.split(cli_entry)
        expected_dict = dict(expected)
    else:
        params = shlex.split(cli_entry) + " ".join(base.splitlines()).split()
        expected_dict = {**dict(expected), **dict(BASE_EXPECTED)}

    env_vars = {}
    for entry in NavigatorConfiguration.entries:
        env_var_name = entry.environment_variable("ansible_navigator")
        env_var_value = [value.values[1] for value in ENV_VAR_DATA if value.values[0] == entry.name]
        assert len(env_var_value) == 1, entry.name
        env_vars[env_var_name] = env_var_value[0]

    for env_var, env_value in env_vars.items():
        if not isinstance(env_value, str):
            msg = "Unexpected data"
            raise pytest.fail(msg)
        monkeypatch.setenv(env_var, env_value)

    response = generate_config(params=params, settings_file_name=settings)
    assert response.exit_messages == []
    for key, value in expected_dict.items():
        configured_entry = response.application_configuration.entry(key)
        assert configured_entry.value.current == value, configured_entry.name
        assert configured_entry.value.source is C.USER_CLI, configured_entry.name
    for entry in response.application_configuration.entries:
        if entry.name not in expected_dict:
            assert entry.value.source is C.ENVIRONMENT_VARIABLE, entry.name


@pytest.mark.usefixtures("_ansible_version")
@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_default(
    monkeypatch: pytest.MonkeyPatch,
    generate_config: GenerateConfigCallable,
    entry: SettingsEntry,
) -> None:
    """Ensure all entries are set to a default value.

    Args:
        monkeypatch: Pytest monkeypatch fixture
        generate_config: Fixture for generating a config
        entry: Settings entry
    """
    monkeypatch.setattr("shutil.which", which)

    response = generate_config()
    assert response.exit_messages == []
    configured_entry = response.application_configuration.entry(entry.name)
    if configured_entry.value.default is C.NOT_SET:
        assert configured_entry.value.source is C.NOT_SET, configured_entry
    elif configured_entry.name == "playbook_save_as":
        assert configured_entry.value.source is C.DEFAULT_CFG, configured_entry
        assert configured_entry.value.current.endswith(entry.value.default), configured_entry
    elif configured_entry.name == "container_engine":
        assert configured_entry.value.source is C.AUTO, configured_entry
        assert configured_entry.value.current == "podman"
    else:
        assert configured_entry.value.source is C.DEFAULT_CFG, configured_entry
        assert configured_entry.value.current == entry.value.default, configured_entry


@pytest.mark.usefixtures("_ansible_version")
@pytest.mark.parametrize(("settings", "settings_file_type"), SETTINGS)
@pytest.mark.parametrize(("entry", "value", "expected"), ENV_VAR_DATA)
def test_all_entries_reflect_env_var_given_settings(
    monkeypatch: pytest.MonkeyPatch,
    generate_config: GenerateConfigCallable,
    settings: str,
    settings_file_type: str,
    entry: str,
    value: str,
    expected: str | list[str],
) -> None:
    """Ensure each entry is are set by an environment variables.

    Even though settings file has been provided, the others
    should by default or settings file

    Args:
        monkeypatch: Pytest monkeypatch fixture
        generate_config: Fixture for generating a config
        settings: Settings file name
        settings_file_type: Settings file type
        entry: Entry name
        value: Value to set
        expected: Expected value
    """
    monkeypatch.setattr("shutil.which", which)
    monkeypatch.setattr("os.path.isfile", isfile)
    environment_variable = NavigatorConfiguration.entry(entry).environment_variable(
        "ansible_navigator",
    )

    monkeypatch.setenv(environment_variable, str(value))
    response = generate_config(settings_file_name=settings)
    assert response.exit_messages == []
    configured_entry = response.application_configuration.entry(entry)
    assert configured_entry.value.source is C.ENVIRONMENT_VARIABLE
    assert configured_entry.value.current == expected

    for other_entry in response.application_configuration.entries:
        if other_entry.name != entry:
            if settings_file_type == "empty":
                if other_entry.value.default is C.NOT_SET:
                    assert other_entry.value.source is C.NOT_SET, other_entry.name
                elif other_entry.value.default == "auto":
                    assert other_entry.value.source is C.AUTO, other_entry.name
                else:
                    assert other_entry.value.source is C.DEFAULT_CFG, other_entry.name
            elif settings_file_type == "full":
                assert other_entry.value.source is C.USER_CFG, other_entry.name


@pytest.mark.usefixtures("_ansible_version")
@pytest.mark.parametrize("entry", NavigatorConfiguration.entries, ids=id_for_name)
def test_all_entries_reflect_settings_given_settings(
    monkeypatch: pytest.MonkeyPatch,
    generate_config: GenerateConfigCallable,
    entry: SettingsEntry,
) -> None:
    """Ensure all entries are set to an entry in a settings file.

    Args:
        monkeypatch: Pytest monkeypatch fixture
        generate_config: Fixture for generating a config
        entry: Settings entry
    """
    monkeypatch.setattr("shutil.which", which)
    monkeypatch.setattr("os.path.isfile", isfile)
    response = generate_config(settings_file_name="ansible-navigator.yml")
    assert response.exit_messages == []
    configured_entry = response.application_configuration.entry(entry.name)
    if entry.cli_parameters is not None:
        assert configured_entry.value.source is C.USER_CFG, configured_entry
        path = entry.settings_file_path("ansible-navigator")
        expected = config_post_process(response.settings_contents, path)

        for key in path.split("."):
            expected = expected[key]
        assert configured_entry.value.current == expected, configured_entry
