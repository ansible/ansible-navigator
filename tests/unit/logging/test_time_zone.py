"""Tests for time zone support in the log."""

import re

from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Optional
from typing import Pattern

import pytest

from ansible_navigator import cli


@dataclass
class Scenario:
    """Data for time zone support in the logs."""

    re_match: Pattern
    time_zone: Optional[str] = None
    will_exit: bool = False

    def __str__(self):
        """Provide the test id.

        :returns: The test id
        """
        return f"{self.time_zone}"

    def args(self, log_file: Path) -> List[str]:
        """Provide an argument list for the CLI.

        :param log_file: The path to the lgo file
        :returns: The list of CLI arguments
        """
        arg_list = ["ansible-navigator", "--la", "false", "--lf", str(log_file), "--ll", "debug"]
        if isinstance(self.time_zone, str):
            arg_list.extend(["--tz", self.time_zone])
        return arg_list


test_data = (
    Scenario(re_match=re.compile(r"^.*\+00:00$")),
    Scenario(re_match=re.compile(r"^.*-0[78]:00$"), time_zone="America/Los_Angeles"),
    Scenario(re_match=re.compile(r"^.*\+09:00$"), time_zone="Japan"),
    Scenario(re_match=re.compile(r"^.*[+-][01][0-9]:[0-5][0-9]$"), time_zone="local"),
    Scenario(re_match=re.compile(r"^.*\+00:00$"), time_zone="does_not_exist", will_exit=True),
)


@pytest.mark.parametrize("data", test_data, ids=str)
def test(
    data: Scenario,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    """Start with the CLI, create log messages and match the time zone.

    :param caplog: The log capture fixture
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
    assert all(data.re_match.match(record.asctime) for record in caplog.records)
