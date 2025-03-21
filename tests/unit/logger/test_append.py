"""Tests for appending to the log."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any

import pytest

from ansible_navigator import cli
from tests.defaults import BaseScenario
from tests.defaults import id_func


if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class Scenario(BaseScenario):
    """Data for the log append tests."""

    name: str
    log_append: bool
    repeat: int = 5
    session_count: int = 1

    def __str__(self) -> str:
        """Provide the test id.

        Returns:
            The test id
        """
        return f"{self.log_append}"

    def args(self, log_file: Path) -> list[str]:
        """Provide an argument list for the CLI.

        Args:
            log_file: The path to the log file

        Returns:
            The list of CLI arguments
        """
        arg_list = [
            "ansible-navigator",
            "--la",
            str(self.log_append),
            "--lf",
            str(log_file),
            "--ll",
            "info",
        ]
        return arg_list


test_data = (
    Scenario(name="0", log_append=True, session_count=5),
    Scenario(name="1", log_append=False, session_count=1),
)


@pytest.mark.parametrize("data", test_data, ids=id_func)
def test_log_append(data: Scenario, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Start with the CLI, create log messages and count.

    Args:
        data: The test data
        monkeypatch: The monkeypatch fixture
        tmp_path: A temporary file path
    """

    def return_none(*_args: Any, **_kwargs: dict[str, Any]) -> None:
        """Take no action, return none.

        Args:
            *_args: Arguments
            **_kwargs: Keyword arguments

        Returns:
            Nothing
        """
        return

    new_session_msg = "New ansible-navigator instance"
    log_file = tmp_path / "ansible-navigator.log"

    args = data.args(log_file=log_file)
    monkeypatch.setattr("sys.argv", args)
    monkeypatch.setattr("ansible_navigator.cli.wrapper", return_none)

    for _ in range(data.repeat):
        cli.main()
        # prevent multiple handlers
        cli.logger.handlers.clear()
    assert log_file.read_text().count(new_session_msg) == data.session_count
