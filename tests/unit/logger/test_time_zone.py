"""Tests for time zone support in the log."""

from __future__ import annotations

import re

from dataclasses import dataclass
from pathlib import Path
from re import Pattern
from typing import Any

import pytest

from ansible_navigator import cli
from tests.defaults import BaseScenario


@dataclass
class Scenario(BaseScenario):
    """Data for time zone support in the logs."""

    name: str
    re_match: Pattern[str]
    time_zone: str | None = None
    will_exit: bool = False

    def __str__(self) -> str:
        """Provide the test id.

        :returns: The test id
        """
        return f"{self.time_zone}"

    def args(self, log_file: Path) -> list[str]:
        """Provide an argument list for the CLI.

        :param log_file: The path to the lgo file
        :returns: The list of CLI arguments
        """
        arg_list = ["ansible-navigator", "--la", "false", "--lf", str(log_file), "--ll", "debug"]
        if isinstance(self.time_zone, str):
            arg_list.extend(["--tz", self.time_zone])
        return arg_list


test_data = (
    pytest.param(Scenario(name="0", re_match=re.compile(r"^.*\+00:00$")), id="0"),
    pytest.param(
        Scenario(name="1", re_match=re.compile(r"^.*-0[78]:00$"), time_zone="America/Los_Angeles"),
        id="1",
    ),
    pytest.param(
        Scenario(name="2", re_match=re.compile(r"^.*\+09:00$"), time_zone="Japan"), id="2"
    ),
    pytest.param(
        Scenario(name="3", re_match=re.compile(r"^.*[+-][01][0-9]:[0-5][0-9]$"), time_zone="local"),
        id="3",
    ),
    pytest.param(
        Scenario(
            name="4",
            re_match=re.compile(r"^.*\+00:00$"),
            time_zone="does_not_exist",
            will_exit=True,
        ),
        id="4",
    ),
)


@pytest.mark.parametrize("data", test_data)
def test_tz_support(
    data: Scenario,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Start with the CLI, create log messages and match the time zone.

    :param caplog: The log capture fixture
    :param data: The test data
    :param monkeypatch: The monkeypatch fixture
    :param tmp_path: A temporary file path
    """

    def return_none(*_args: Any, **_kwargs: dict[str, Any]) -> None:
        """Take no action, return none.

        :param _args: Arguments
        :param _kwargs: Keyword arguments
        :returns: Nothing
        """
        return

    log_file = tmp_path / "ansible-navigator.log"
    args = data.args(log_file=log_file)
    monkeypatch.setattr("sys.argv", args)
    monkeypatch.setattr("ansible_navigator.cli.wrapper", return_none)

    if data.will_exit:
        with pytest.raises(SystemExit):
            cli.main()
    else:
        cli.main()
    # This is a conservative number based on debug logging, it should be closer to 200
    # but this assertion is here to ensure many records were retrieved.
    assert len(caplog.records) > 100
    for record in caplog.records:
        assert data.re_match.match(
            record.asctime
        ), f"{data.re_match.pattern} does not match '{record.asctime}'"
