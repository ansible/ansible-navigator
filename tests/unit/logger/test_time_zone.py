"""Tests for time zone support in the log."""

from __future__ import annotations

import re

from dataclasses import dataclass
from re import Pattern
from typing import TYPE_CHECKING

import pytest

from ansible_navigator.utils.functions import shlex_join
from tests.defaults import BaseScenario


if TYPE_CHECKING:
    from pathlib import Path

    from tests.conftest import TCmdInTty


@dataclass
class Scenario(BaseScenario):
    """Data for time zone support in the logs."""

    name: str
    re_match: Pattern[str]
    time_zone: str | None = None
    will_exit: bool = False

    def __str__(self) -> str:
        """Provide the test id.

        Returns:
            The test id
        """
        return f"{self.time_zone}"

    def args(self, log_file: Path) -> list[str]:
        """Provide an argument list for the CLI.

        Args:
            log_file: The path to the lgo file

        Returns:
            The list of CLI arguments
        """
        arg_list = [
            "ansible-navigator",
            "--la",
            "false",
            "--lf",
            str(log_file),
            "--ll",
            "debug",
            "--mode",
            "stdout",
            "config",
            "--help-config",
        ]
        if isinstance(self.time_zone, str):
            arg_list.extend(["--tz", self.time_zone])
        return arg_list


test_data = (
    pytest.param(Scenario(name="0", re_match=re.compile(r"^.*\+00:00")), id="0"),
    pytest.param(
        Scenario(name="1", re_match=re.compile(r"^.*-0[78]:00"), time_zone="America/Los_Angeles"),
        id="1",
    ),
    pytest.param(
        Scenario(name="2", re_match=re.compile(r"^.*\+09:00"), time_zone="Japan"),
        id="2",
    ),
    pytest.param(
        Scenario(name="3", re_match=re.compile(r"^.*[+-][01][0-9]:[0-5][0-9]"), time_zone="local"),
        id="3",
    ),
    pytest.param(
        Scenario(
            name="4",
            re_match=re.compile(r"^.*\+00:00"),
            time_zone="does_not_exist",
            will_exit=True,
        ),
        id="4",
    ),
)


@pytest.mark.parametrize("data", test_data)
def test_tz_support(
    data: Scenario,
    cmd_in_tty: TCmdInTty,
    tmp_path: Path,
) -> None:
    """Start with the CLI, create log messages and match the time zone.

    Args:
        data: The test data
        cmd_in_tty: The tty command runner
        tmp_path: A temporary file path
    """
    log_file = tmp_path / "ansible-navigator.log"
    args = data.args(log_file=log_file)
    command = shlex_join(args)
    stdout, stderr, exit_code = cmd_in_tty(cmd=command)
    if data.will_exit:
        assert exit_code != 0, f"{stdout}, {stderr}, {exit_code}"
    else:
        assert exit_code == 0, f"{stdout}, {stderr}, {exit_code}"
    for line in log_file.read_text().splitlines():
        assert data.re_match.match(
            line,
        ), f"{data.re_match.pattern} does not match '{line}'"
