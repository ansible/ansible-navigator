"""Check diagnostics output."""

from __future__ import annotations

import json
import subprocess

from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pytest

    from ansible_navigator.configuration_subsystem.definitions import SettingsFileType

from ansible_navigator.utils.functions import remove_ansi


def test(
    monkeypatch: pytest.MonkeyPatch,
    settings_env_var_to_full: tuple[Path, SettingsFileType],
    tmp_path: Path,
    skip_if_already_failed: None,
) -> None:
    """Test diagnostics generation.

    Args:
        monkeypatch: Fixture for patching
        settings_env_var_to_full: The pytest subtest fixture
        tmp_path: The pytest tmp_path fixture
        skip_if_already_failed: Fixture that stops parametrized tests running on first failure.

    Raises:
        AssertionError: When tests fails
    """
    monkeypatch.chdir(tmp_path)
    settings_path, settings_file = settings_env_var_to_full

    proc_out = subprocess.run(
        "ansible-navigator --diagnostics",  # noqa:S607
        check=False,
        shell=True,
        capture_output=True,
        text=True,
    )
    stdout_lines = proc_out.stdout.splitlines()
    assert "Diagnostics written to: " in stdout_lines[-1]

    file_name = remove_ansi(stdout_lines[-1].split(":", 1)[-1].strip())
    full_path = tmp_path / file_name
    contents = full_path.read_text()
    diagnostics = json.loads(contents)

    assert diagnostics["settings_file"]["contents"] == settings_file
    local_env_vars = diagnostics["local_system"]["details"]["environment_variables"]
    assert local_env_vars["details"]["ANSIBLE_NAVIGATOR_CONFIG"] == str(settings_path)
    for section in diagnostics.values():
        assert not section.get("errors")

    # Test the file permissions as well since diagnostics takes time to run
    status = Path(file_name).stat()
    assert oct(status.st_mode)[-3:] == str(oct(0o600))[-3:]
