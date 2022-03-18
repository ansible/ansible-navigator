"""Check exit messages for json schema validation."""
import os
import subprocess

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Tuple

import pytest

from ansible_navigator.utils.functions import shlex_join
from ...defaults import FIXTURES_DIR


TEST_FIXTURE_DIR = Path(FIXTURES_DIR) / "unit" / "configuration_subsystem"


@dataclass
class Scenario:
    """Data for the tests."""

    comment: str
    """The comment for the test"""
    settings_file: Path
    """The settings file path"""
    messages: Tuple[str, ...]
    """Messages expected to be found"""

    command: Tuple[str, ...] = ("ansible-navigator", "-m", "stdout")
    """The command to run"""

    def __str__(self):
        """Provide a test id.

        :returns: The test id
        """
        return self.comment


test_data = (
    Scenario(
        comment="Empty settings file",
        messages=("Settings file cannot be empty",),
        settings_file=TEST_FIXTURE_DIR / "ansible-navigator_broken.yml",
    ),
    Scenario(
        comment="Unrecognized key",
        messages=("'unknown' was unexpected",),
        settings_file=TEST_FIXTURE_DIR / "ansible-navigator_unknown_key.yml",
    ),
    Scenario(
        comment="Unrecognized app",
        messages=("'non_app' is not one of ['builder',",),
        settings_file=TEST_FIXTURE_DIR / "ansible-navigator_no_app.yml",
    ),
    Scenario(
        comment="EE enabled is not a bool",
        messages=("5 is not one of [True, False]",),
        settings_file=TEST_FIXTURE_DIR / "ansible-navigator_not_bool.yml",
    ),
)


@pytest.mark.parametrize("data", test_data, ids=str)
def test(data: Scenario, subtests: Any, tmp_path: Path):
    """Test for json schema errors.

    :param data: The test data
    :param tmp_path: The temporary path fixture
    :param subtests: The pytest subtest fixture

    :raises AssertionError: When tests fails
    """
    assert data.settings_file.exists()
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path is None:
        raise AssertionError(
            "VIRTUAL_ENV environment variable was not set but tox should have set it.",
        )
    venv = Path(venv_path, "bin", "activate")
    log_file = tmp_path / "log.txt"

    command = list(data.command) + ["--lf", str(log_file)]

    bash_wrapped = f"/bin/bash -c 'source {venv!s} && {shlex_join(command)}'"
    env = {"ANSIBLE_NAVIGATOR_CONFIG": str(data.settings_file), "NO_COLOR": "true"}
    proc_out = subprocess.run(
        bash_wrapped,
        check=False,
        env=env,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    for value in data.messages:
        with subtests.test(msg=value, value=value):
            assert value in proc_out.stdout
