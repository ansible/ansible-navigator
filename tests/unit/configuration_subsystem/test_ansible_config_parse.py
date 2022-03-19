"""Test the basic parsing of an ansible.cfg file."""
from copy import deepcopy
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import NavigatorConfiguration
from ansible_navigator.configuration_subsystem.utils import parse_ansible_cfg


ee_states = pytest.mark.parametrize(
    argnames="ee_enabled", argvalues=(True, False), ids=("ee_true", "ee_false")
)

ANSIBLE_CFG_VALID = """
[defaults]

cow_selection = milk
inventory = inventory.yml
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_valid(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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
        "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"}
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
        "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"}
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
        assert not parsed_cfg.config.contents
        assert not parsed_cfg.config.path
        assert not parsed_cfg.config.text
    else:
        assert parsed_cfg.config.contents == {
            "defaults": {"cow_selection": "milk", "inventory": "inventory.yml"}
        }
        assert parsed_cfg.config.path == cfg_path
        assert parsed_cfg.config.text == ANSIBLE_CFG_VALID.splitlines()


ANSIBLE_CFG_INVALID = """
[defaults]

12345
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_invalid(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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

    assert not parsed_cfg.config.contents
    assert not parsed_cfg.config.path
    assert not parsed_cfg.config.text
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

    assert not application_configuration.internals.ansible_configuration.contents
    assert not application_configuration.internals.ansible_configuration.path
    assert not application_configuration.internals.ansible_configuration.text
    assert "12345" in exit_messages[2].message
