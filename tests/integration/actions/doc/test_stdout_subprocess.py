"""Test doc using subprocess."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from ansible_navigator.utils.functions import shlex_join
from tests.defaults import BaseScenario
from tests.defaults import id_func
from ....conftest import TCmdInTty


BUILTINS = (
    "validate_argument_spec",
    "wait_for_connection",
    "yum_repository",
)


@dataclass(frozen=True)
class StdoutCliTest(BaseScenario):
    """Definition of a stdout cli test."""

    comment: str
    """Description of the test"""
    params: tuple[str, ...]
    """Parameters for the subcommand"""
    expected: tuple[str, ...] = BUILTINS
    """Expected output"""
    subcommand: str = "doc"

    def __str__(self) -> str:
        """Provide a test id.

        :returns: The test id
        """
        return self.comment

    @property
    def command(self) -> tuple[str, ...]:
        """Provide the constructed command.

        :returns: The constructed command
        """
        return ("ansible-navigator", self.subcommand) + self.params


# Intentionally not using parametrize so the behavior can be documented
StdoutCliTests = (
    StdoutCliTest(
        comment="-l",
        params=("-l",),
    ),
    StdoutCliTest(
        comment="--list",
        params=("--list",),
    ),
    StdoutCliTest(
        comment="-F",
        params=("-F",),
    ),
    StdoutCliTest(
        comment="--list_files",
        params=("--list_files",),
    ),
    StdoutCliTest(
        comment="-s",
        params=(
            "debug",
            "-s",
        ),
        expected=(
            "name:",
            "debug:",
            "msg:",
        ),
    ),
    StdoutCliTest(
        comment="--snippet",
        params=(
            "debug",
            "--snippet",
        ),
        expected=(
            "name:",
            "debug:",
            "msg:",
        ),
    ),
    StdoutCliTest(
        comment="--metadata-dump",
        params=("--metadata-dump",),
    ),
)


@pytest.mark.usefixtures("use_venv")
@pytest.mark.parametrize(argnames="data", argvalues=StdoutCliTests, ids=id_func)
@pytest.mark.parametrize(argnames="exec_env", argvalues=(True, False), ids=("ee_true", "ee_false"))
def test(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    data: StdoutCliTest,
    exec_env: bool,
    cmd_in_tty: TCmdInTty,
) -> None:
    """Test doc using subcommand.

    :param monkeypatch: The monkeypatch fixture
    :param tmp_path: The temporary path to use
    :param data: The test data
    :param exec_env: Whether to use the exec environment
    :param cmd_in_tty: The tty command runner
    :raises AssertionError: When test fails
    """
    log_file = str(tmp_path / "log.txt")
    monkeypatch.setenv("PAGER", "cat")
    monkeypatch.setenv("NO_COLOR", "true")
    command = shlex_join(
        data.command + ("--lf", log_file, "--ee", str(exec_env), "--set-env", "PAGER=cat"),
    )
    stdout, _stderr, _exit_code = cmd_in_tty(cmd=command)

    assert all(d in stdout for d in data.expected)
