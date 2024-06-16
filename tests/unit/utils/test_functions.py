"""Test the functions exposed in the :mod:`~ansible_navigator.utils.functions` subpackage."""

from __future__ import annotations

import re

from pathlib import Path
from typing import Any
from typing import NamedTuple

import pytest

from ansible_navigator.data.catalog_collections import get_doc_withast
from ansible_navigator.utils.functions import environment_variable_is_file_path
from ansible_navigator.utils.functions import expand_path
from ansible_navigator.utils.functions import find_settings_file
from ansible_navigator.utils.functions import flatten_list
from ansible_navigator.utils.functions import human_time
from ansible_navigator.utils.functions import now_iso
from ansible_navigator.utils.functions import oxfordcomma
from ansible_navigator.utils.functions import path_is_relative_to
from ansible_navigator.utils.functions import round_half_up
from ansible_navigator.utils.functions import unescape_moustaches


EXTENSIONS = [".yml", ".yaml", ".json"]


def test_find_many_settings_home(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test more than one in home.

    :param monkeypatch: The monkeypatch fixture
    """
    home_path = Path.home() / ".ansible-navigator"
    paths = [Path(f"{home_path}{ext}") for ext in EXTENSIONS]

    def check_path_exists(arg: Any) -> bool:
        return arg in paths

    monkeypatch.setattr(Path, "exists", check_path_exists)
    _messages, exit_messages, _found = find_settings_file()
    expected = f"Only one file among {oxfordcomma(paths, 'and')}"
    assert any(expected in exit_msg.message for exit_msg in exit_messages)


def test_find_many_settings_cwd(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test more than one in CWD.

    :param monkeypatch: The monkeypatch fixture
    """
    cwd_path = Path.cwd() / "ansible-navigator"
    paths = [Path(f"{cwd_path}{ext}") for ext in EXTENSIONS]

    def check_path_exists(arg: Any) -> bool:
        return arg in paths

    monkeypatch.setattr(Path, "exists", check_path_exists)
    _messages, exit_messages, _found = find_settings_file()
    expected = f"Only one file among {oxfordcomma(paths, 'and')}"
    assert any(expected in exit_msg.message for exit_msg in exit_messages)


def test_find_many_settings_precedence(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test more than one in CWD.

    :param monkeypatch: The monkeypatch fixture
    """
    expected = Path.cwd() / "ansible-navigator.yml"
    paths = [expected, Path.home() / ".ansible-navigator.json"]

    def check_path_exists(arg: Any) -> bool:
        return arg in paths

    monkeypatch.setattr(Path, "exists", check_path_exists)
    _messages, _exit_messages, found = find_settings_file()
    assert expected == found


@pytest.mark.parametrize(
    ("set_env", "file_path", "anticipated_result"),
    (
        (True, str(expand_path(__file__)), str(expand_path(__file__))),
        (True, "", None),
        (False, None, None),
    ),
    ids=[
        "set-and-valid",
        "set-and-invalid",
        "not-set",
    ],
)
def test_env_var_is_file_path(
    monkeypatch: pytest.MonkeyPatch,
    set_env: bool,
    file_path: str,
    anticipated_result: str | None,
) -> None:
    """Test environment variable is a file path.

    :param monkeypatch: The monkeypatch fixture
    :param set_env: To set or not to set the env var
    :param file_path: File path to set env var to
    :param anticipated_result: Expected outcome for assertion
    """
    env_var = "ANSIBLE_NAVIGATOR_CONFIG"
    if set_env:
        monkeypatch.setenv(env_var, file_path)
    _messages, _exit_messages, result = environment_variable_is_file_path(
        env_var,
        "config",
    )
    assert result == anticipated_result


@pytest.mark.parametrize(
    ("value", "anticipated_result"),
    (
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, [3]], [1, 2, 3]),
        ([1, [2], [3, 4], 5, True, {6: False}], [1, 2, 3, 4, 5, True, {6: False}]),
    ),
    ids=[
        "simple",
        "list-with-one-list",
        "list-detailed",
    ],
)
def test_flatten_list(value: list[str], anticipated_result: list[str]) -> None:
    """Test for flatten list.

    :param value: List to be flattened
    :param anticipated_result: Expected outcome for assertion
    """
    actual_result = flatten_list(value)
    assert list(actual_result) == anticipated_result


class HumanTimeTestData(NamedTuple):
    """Data for human time test."""

    value: int | float
    expected: str


human_time_test_data = [
    pytest.param(HumanTimeTestData(value=1, expected="1s"), id="s"),
    pytest.param(HumanTimeTestData(value=60 + 1, expected="1m1s"), id="ms"),
    pytest.param(HumanTimeTestData(value=3600 + 60 + 1, expected="1h1m1s"), id="hms"),
    pytest.param(
        HumanTimeTestData(
            value=86400 + 3600 + 60 + 1,
            expected="1d1h1m1s",
        ),
        id="d-hms",
    ),
]


@pytest.mark.parametrize("data", human_time_test_data)
def test_human_time_integer(data: HumanTimeTestData) -> None:
    """Test for the functions.human_time function (integer passed).

    Ensure the integer passed is correctly transformed into a human readable time string.

    :param data: Time data in human-readable format
    """
    result = human_time(data.value)
    assert result == data.expected


@pytest.mark.parametrize("data", human_time_test_data)
def test_human_time_negative_integer(data: HumanTimeTestData) -> None:
    """Test for the functions.human_time function (negative integer passed).

    Ensure the negative integer passed is correctly transformed into a human readable time string.

    :param data: Time data in human-readable format
    """
    result = human_time(-data.value)
    assert result == f"-{data.expected}"


@pytest.mark.parametrize("data", human_time_test_data)
def test_human_time_float(data: HumanTimeTestData) -> None:
    """Test for the functions.human_time function (float passed).

    Ensure the float passed is correctly transformed into a human readable time string.

    :param data: Time data in human-readable format
    """
    result = human_time(float(data.value))
    assert result == data.expected


@pytest.mark.parametrize("data", human_time_test_data)
def test_human_time_negative_float(data: HumanTimeTestData) -> None:
    """Test for the functions.human_time function (negative float passed).

    Ensure the negative float passed is correctly transformed into a human readable time string.

    :param data: Time data in human-readable format
    """
    result = human_time(-float(data.value))
    assert result == f"-{data.expected}"


class RoundHalfUpTestData(NamedTuple):
    """Data for round half up tests."""

    id_: str
    value: int | float
    expected: int


round_half_up_test_data = [
    RoundHalfUpTestData(id_="integer", value=1, expected=1),
    RoundHalfUpTestData(id_="negative-integer", value=-1, expected=-1),
    RoundHalfUpTestData(id_="down-float", value=1.49999999, expected=1),
    RoundHalfUpTestData(id_="up-float", value=1.50000001, expected=2),
    RoundHalfUpTestData(id_="negative-down-float", value=-1.49999999, expected=-1),
    RoundHalfUpTestData(id_="negative-up-float", value=-1.50000001, expected=-2),
    RoundHalfUpTestData(id_="half_even", value=2.5, expected=3),
    RoundHalfUpTestData(id_="half_even", value=3.5, expected=4),
]


@pytest.mark.parametrize("data", round_half_up_test_data, ids=lambda data: data.id_)
def test_round_half_up(data: RoundHalfUpTestData) -> None:
    """Test for the functions.round_half_up function.

    Ensure the number passed is consistently rounded to the nearest
    integer with ties going away from zero.

    :param data: Test object
    """
    result = round_half_up(data.value)
    assert result == data.expected


def test_path_is_relative_to() -> None:
    """Ensure path_is_relative_to returns accurate results."""
    directory = Path("/tmp/test")
    file_in_directory = Path("/tmp/test/file.txt")
    assert path_is_relative_to(child=file_in_directory, parent=directory)
    assert not path_is_relative_to(child=directory, parent=file_in_directory)


iso8601 = re.compile(
    r"""
    ^
    (?P<year>-?(?:[1-9][0-9]*)?[0-9]{4})-
    (?P<month>1[0-2]|0[1-9])-
    (?P<day>3[01]|0[1-9]|[12][0-9])
    T
    (?P<hour>2[0-3]|[01][0-9]):
    (?P<minute>[0-5][0-9]):
    (?P<second>[0-5][0-9])
    (?P<ms>\.[0-9]+)?
    (?P<timezone>Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?
    $""",
    re.VERBOSE,
)


@pytest.mark.parametrize(
    "time_zone",
    (
        pytest.param("local", id="0"),
        pytest.param("America/Los_Angeles", id="1"),
        pytest.param("UTC", id="2"),
        pytest.param("bogus", id="3"),
    ),
)
def test_now_iso(caplog: pytest.LogCaptureFixture, time_zone: str) -> None:
    """Test the using local as a time zone.

    :param caplog: The log capture fixture
    :param time_zone: The timezone
    """
    time_string = now_iso(time_zone=time_zone)
    re_matched = iso8601.match(time_string)
    assert re_matched is not None
    matched = re_matched.groupdict()
    assert len(matched["year"]) == 4
    assert len(matched["month"]) == 2
    assert len(matched["day"]) == 2
    assert len(matched["hour"]) == 2
    assert len(matched["minute"]) == 2
    assert len(matched["second"]) == 2
    assert matched.get("ms", ".").startswith(".")
    assert len(matched["timezone"]) == 6
    if time_zone == "America/Los_Angeles":
        assert matched["timezone"] in ("-08:00", "-07:00")
    if time_zone == "UTC":
        assert matched["timezone"] == "+00:00"
    if time_zone == "bogus":
        assert matched["timezone"] == "+00:00"
        assert "The time zone 'bogus' could not be found. Using UTC." in caplog.text


@pytest.mark.parametrize(
    ("data", "output"),
    (
        pytest.param({}, {}, id="0"),
        pytest.param(None, None, id="1"),
        pytest.param([], [], id="2"),
        pytest.param("foo", "foo", id="3"),
    ),
)
def test_unescape_moustaches(data: Any, output: Any) -> None:
    """Tests unescape_moustaches.

    :param data: The input data.
    :param output: The expected output.
    """
    result = unescape_moustaches(data)
    assert result == output


def test_get_doc_withast() -> None:
    """Test for the get_doc_withast function.

    This test ensures that the get_doc_withast function correctly extracts the documentation,
    examples, returndocs, and metadata from the module content.
    """
    module_content = """
DOCUMENTATION = "This is a test documentation."
EXAMPLES = "Example usage here."
RETURN = "This function returns a value."
METADATA = "Author: John Doe"
"""

    doc, examples, returndocs, metadata = get_doc_withast(module_content)
    assert doc == "This is a test documentation."
    assert examples == "Example usage here."
    assert returndocs == "This function returns a value."
    assert metadata == "Author: John Doe"
