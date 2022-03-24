"""Test the basic parsing of an ansible.cfg file."""
from copy import deepcopy
from pathlib import Path

import pytest

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner.command_runner import run_command
from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.utils import parse_ansible_cfg


ee_states = pytest.mark.parametrize(
    argnames="ee_enabled",
    argvalues=(True, False),
    ids=("ee_true", "ee_false"),
)

ANSIBLE_CFG_VALID = """
[defaults]

cow_selection = milk
inventory = inventory.yml
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid_config(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a valid ansible.cfg is parsed.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "ansible.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(ANSIBLE_CFG_VALID)
    monkeypatch.chdir(tmp_path)
    parsed_cfg = parse_ansible_cfg(ee_enabled=ee_enabled)

    assert parsed_cfg.config.contents == {
        "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"},
    }
    assert parsed_cfg.config.path == cfg_path
    assert parsed_cfg.config.text == ANSIBLE_CFG_VALID.splitlines()


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid_configurator(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a valid ansible.cfg is parsed using configurator.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "ansible.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(ANSIBLE_CFG_VALID)
    monkeypatch.chdir(tmp_path)
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        params=["--ee", str(ee_enabled)],
        application_configuration=application_configuration,
    )
    configurator.configure()

    assert application_configuration.internals.ansible_configuration.contents == {
        "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"},
    }
    assert application_configuration.internals.ansible_configuration.path == cfg_path
    assert (
        application_configuration.internals.ansible_configuration.text
        == ANSIBLE_CFG_VALID.splitlines()
    )


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid_home(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a valid .ansible.cfg is parsed when in the home directory.

    When EE support is enabled, the .ansible.cfg file is not used
    When EE support is disabled the .ansible.cfg file is used

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / ".ansible.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(ANSIBLE_CFG_VALID)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))

    parsed_cfg = parse_ansible_cfg(ee_enabled=ee_enabled)

    if ee_enabled:
        assert parsed_cfg.config.contents is Constants.NONE
        assert parsed_cfg.config.path is Constants.NONE
        assert parsed_cfg.config.text is Constants.NONE
    else:
        assert parsed_cfg.config.contents == {
            "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"},
        }
        assert parsed_cfg.config.path == cfg_path
        assert parsed_cfg.config.text == ANSIBLE_CFG_VALID.splitlines()


ANSIBLE_CFG_INVALID = """
[defaults]

12345
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_invalid_config(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a invalid ansible.cfg raises errors.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "ansible.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(ANSIBLE_CFG_INVALID)
    monkeypatch.chdir(tmp_path)
    parsed_cfg = parse_ansible_cfg(ee_enabled=ee_enabled)

    assert parsed_cfg.config.contents is Constants.NONE
    assert parsed_cfg.config.path is Constants.NONE
    assert parsed_cfg.config.text is Constants.NONE
    assert "12345" in parsed_cfg.exit_messages[1].message


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_invalid_configurator(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm a invalid ansible.cfg raises errors using configurator.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    cfg_path = tmp_path / "ansible.cfg"
    with cfg_path.open(mode="w") as fh:
        fh.write(ANSIBLE_CFG_INVALID)
    monkeypatch.chdir(tmp_path)
    application_configuration = deepcopy(NavigatorConfiguration)
    application_configuration.internals.initializing = True
    configurator = Configurator(
        params=["--ee", str(ee_enabled)],
        application_configuration=application_configuration,
    )
    _messages, exit_messages = configurator.configure()

    assert application_configuration.internals.ansible_configuration.contents is Constants.NONE
    assert application_configuration.internals.ansible_configuration.path is Constants.NONE
    assert application_configuration.internals.ansible_configuration.text is Constants.NONE
    assert "12345" in exit_messages[2].message


@pytest.mark.usefixtures("ansible_version")
@ee_states
def test_config_none(ee_enabled):
    """Confirm a invalid ansible.cfg raises errors.

    :param ee_enabled: Indicate if EE support is enabled
    """
    parsed_cfg = parse_ansible_cfg(ee_enabled=ee_enabled)

    assert parsed_cfg.config.contents is Constants.NONE
    assert parsed_cfg.config.path is Constants.NONE
    assert parsed_cfg.config.text is Constants.NONE
    if ee_enabled:
        assert (
            "no 'ansible.cfg' found in current working directory." in parsed_cfg.messages[1].message
        )
    else:
        assert "'ansible --version' reports no config file" in parsed_cfg.messages[2].message


@ee_states
def test_invalid_path(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm an invalid path to ansible.cfg is handled.

    :param ee_enabled: Indicate if EE support is enabled
    :param tmp_path: The path to a test temporary directory
    :param monkeypatch: The monkeypatch fixture
    """
    original_run_command = run_command

    def static_ansible_version(command: Command):
        if command.command == "ansible --version":
            command.return_code = 0
            command.stdout = f"ansible [core 2.12.3]\nconfig file = {(tmp_path / 'ansible.cfg')!s}"
        else:
            original_run_command(command)

    monkeypatch.setattr(
        "ansible_navigator.command_runner.command_runner.run_command",
        static_ansible_version,
    )

    parsed_cfg = parse_ansible_cfg(ee_enabled=ee_enabled)
    assert parsed_cfg.config.contents is Constants.NONE
    assert parsed_cfg.config.path is Constants.NONE
    assert parsed_cfg.config.text is Constants.NONE
    if ee_enabled:
        assert (
            "no 'ansible.cfg' found in current working directory." in parsed_cfg.messages[1].message
        )
    else:
        assert "does not exist" in parsed_cfg.messages[2].message
