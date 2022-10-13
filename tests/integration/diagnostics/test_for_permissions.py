"""Check diagnostics permissions."""
from __future__ import annotations

import os
import subprocess

from pathlib import Path

import pytest

from ansible_navigator.utils.functions import remove_ansi


@pytest.mark.usefixtures("use_venv")
def test(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    """Test diagnostics generation.

    :param monkeypatch: Fixture for patching
    :param settings_env_var_to_full: The pytest subtest fixture
    :param tmp_path: The pytest tmp_path fixture

    :raises AssertionError: When tests fails
    """
    monkeypatch.chdir(tmp_path)

    proc_out = subprocess.run(
        "ansible-navigator --diagnostics",
        check=False,
        shell=True,
        capture_output=True,
        text=True,
    )
    stdout_lines = proc_out.stdout.splitlines()
    assert "Diagnostics written to: " in stdout_lines[-1]

    file_name = remove_ansi(stdout_lines[-1].split(":", 1)[-1].strip())
    status = os.stat(file_name)
    assert oct(status.st_mode)[-3:] == str(oct(0o600))[-3:]
