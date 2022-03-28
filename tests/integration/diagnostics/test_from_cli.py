"""Check diagnostics output."""
import json
import subprocess

from pathlib import Path
from typing import Tuple

import pytest

from ansible_navigator.configuration_subsystem.definitions import SettingsFileType
from ansible_navigator.utils.functions import remove_ansi


@pytest.mark.usefixtures("use_venv")
def test(
    monkeypatch: pytest.MonkeyPatch,
    settings_env_var_to_full: Tuple[Path, SettingsFileType],
    tmp_path: Path,
):
    """Test diagnostics generation.

    :param monkeypatch: Fixture for patching
    :param settings_env_var_to_full: The pytest subtest fixture
    :param tmp_path: The pytest tmp_path fixture

    :raises AssertionError: When tests fails
    """
    monkeypatch.chdir(tmp_path)
    settings_path, settings_file = settings_env_var_to_full

    proc_out = subprocess.run(
        "ansible-navigator --diagnostics",
        check=False,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    stdout_lines = proc_out.stdout.splitlines()
    assert "Diagnostics written to: diagnostics_" in stdout_lines[-1]

    file_name = remove_ansi(stdout_lines[-1].split(":", 1)[-1].strip())
    full_path = tmp_path / file_name
    contents = full_path.read_text()
    diagnostics = json.loads(contents)

    assert diagnostics["settings_file"]["contents"] == settings_file
    assert diagnostics["local_system"]["environment_variables"]["ANSIBLE_NAVIGATOR_CONFIG"] == str(
        settings_path,
    )
    for _section_name, section in diagnostics.items():
        assert not section.get("errors")