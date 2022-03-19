"""Test the use of the ansible.cfg file for inventory."""
from copy import deepcopy
from pathlib import Path

import pytest

from ansible_navigator.configuration_subsystem import Configurator
from ansible_navigator.configuration_subsystem import Constants
from ansible_navigator.configuration_subsystem import NavigatorConfiguration


ee_states = pytest.mark.parametrize(
    argnames="ee_enabled",
    argvalues=(True, False),
    ids=("ee_true", "ee_false"),
)

ANSIBLE_CFG_VALID = """
[defaults]

inventory = inventory.yml,/tmp/inventory.yaml
"""


@pytest.mark.usefixtures("use_venv")
@ee_states
def test_from_ansible_cfg(ee_enabled, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Confirm inventory is used from a valid ansible.cfg.

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
    entry = application_configuration.entry("inventory")
    assert entry.value.source is Constants.ANSIBLE_CFG
    assert entry.value.current == [str(tmp_path / "inventory.yml"), "/tmp/inventory.yaml"]
