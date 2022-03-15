"""Tests for appending to the log."""

from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest

from ansible_navigator import cli


@dataclass
class TestData:
    """Data for the log append tests."""

    log_append: bool
    repeat: int = 5
    session_count: int = 1

    def __str__(self):
        """Provide the test id.

        :returns: The test id
        """
        return f"{self.log_append}"

    def args(self, log_file: Path) -> List[str]:
        """Provide an argument list for the CLI.

        :param log_file: The path to the lgo file
        :returns: The list of CLI arguments
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
    TestData(log_append=True, session_count=5),
    TestData(log_append=False, session_count=1),
)


@pytest.mark.parametrize("data", test_data, ids=str)
def test_log_append(data: TestData, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Start with the CLI, create log messages and count.

    :param data: The test data
    :param monkeypatch: The monkeypatch fixture
    :param tmp_path: A temporary file path
    """

    def return_none(*_args, **_kwargs) -> None:
        """Take no action, return none.

        :param _args: Arguments
        :param _kwargs: Keyword arguments
        :returns: Nothing
        """
        return None

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
