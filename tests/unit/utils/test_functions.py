"""Test the functions exposed in the :mod:`~ansible_navigator.utils` subpackage."""
import os

from pathlib import Path
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Union

import pytest

from ansible_navigator import utils


EXTENSIONS = [".yml", ".yaml", ".json"]


def test_find_many_settings_home(monkeypatch) -> None:
    """test more than one in home"""

    paths = [
        os.path.join(os.path.expanduser("~"), ".ansible-navigator" + ext) for ext in EXTENSIONS
    ]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, exit_messages, _found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any(expected in exit_msg.message for exit_msg in exit_messages)


def test_find_many_settings_cwd(monkeypatch) -> None:
    """test more than one in CWD"""

    paths = [os.path.join(os.getcwd(), "ansible-navigator" + ext) for ext in EXTENSIONS]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, exit_messages, _found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any(expected in exit_msg.message for exit_msg in exit_messages)


def test_find_many_settings_precedence(monkeypatch) -> None:
    """test more than one in CWD"""

    expected = os.path.join(os.getcwd(), "ansible-navigator.yml")
    paths = [expected, os.path.join(os.path.expanduser("~"), ".ansible-navigator.json")]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, _exit_messages, found = utils.find_settings_file()
    assert expected == found


@pytest.mark.parametrize(
    "set_env, file_path, anticpated_result",
    (
        (True, os.path.abspath(__file__), os.path.abspath(__file__)),
        (True, "", None),
        (False, None, None),
    ),
    ids=[
        "set and valid",
        "set and invalid",
        "not set",
    ],
)
def test_env_var_is_file_path(
    monkeypatch,
    set_env: bool,
    file_path: str,
    anticpated_result: Optional[str],
) -> None:
    """test environment variable is a file path"""
    env_var = "ANSIBLE_NAVIGATOR_CONFIG"
    if set_env:
        monkeypatch.setenv(env_var, file_path)
    _messages, _exit_messages, result = utils.environment_variable_is_file_path(env_var, "config")
    assert result == anticpated_result


@pytest.mark.parametrize(
    "value, anticpated_result",
    (
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, [3]], [1, 2, 3]),
        ([1, [2], [3, 4], 5, True, {6: False}], [1, 2, 3, 4, 5, True, {6: False}]),
    ),
    ids=[
        "simple",
        "list with one list",
        "list detailed",
    ],
)
def test_flatten_list(value: List, anticpated_result: List) -> None:
    """test for flatten list"""
    actual_result = utils.flatten_list(value)
    assert list(actual_result) == anticpated_result


class HumanTimeTestData(NamedTuple):
    """Data for human time test."""

    id: str
    value: Union[int, float]
    expected: str


human_time_test_data = [
    HumanTimeTestData(id="seconds", value=1, expected="1s"),
    HumanTimeTestData(id="minutes seconds", value=60 + 1, expected="1m1s"),
    HumanTimeTestData(id="hours minutes seconds", value=3600 + 60 + 1, expected="1h1m1s"),
    HumanTimeTestData(
        id="days hours minutes seconds",
        value=86400 + 3600 + 60 + 1,
        expected="1d1h1m1s",
    ),
]


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_integer(data: HumanTimeTestData) -> None:
    """Test for the utils.human_time function (integer passed).

    Ensure the integer passed is correctly transformed into a human readable time string.
    """
    result = utils.human_time(data.value)
    assert result == data.expected


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_negative_integer(data: HumanTimeTestData) -> None:
    """Test for the utils.human_time function (negative integer passed).

    Ensure the negative integer passed is correctly transformed into a human readable time string.
    """
    result = utils.human_time(-data.value)
    assert result == f"-{data.expected}"


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_float(data: HumanTimeTestData) -> None:
    """Test for the utils.human_time function (float passed).

    Ensure the float passed is correctly transformed into a human readable time string.
    """
    result = utils.human_time(float(data.value))
    assert result == data.expected


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_negative_float(data: HumanTimeTestData) -> None:
    """Test for the utils.human_time function (negative float passed).

    Ensure the negative float passed is correctly transformed into a human readable time string.
    """
    result = utils.human_time(-float(data.value))
    assert result == f"-{data.expected}"


class RoundHalfUpTestData(NamedTuple):
    """Data for round half up tests."""

    id: str
    value: Union[int, float]
    expected: int


round_half_up_test_data = [
    RoundHalfUpTestData(id="integer", value=1, expected=1),
    RoundHalfUpTestData(id="negative integer", value=-1, expected=-1),
    RoundHalfUpTestData(id="down float", value=1.49999999, expected=1),
    RoundHalfUpTestData(id="up float", value=1.50000001, expected=2),
    RoundHalfUpTestData(id="negative down float", value=-1.49999999, expected=-1),
    RoundHalfUpTestData(id="negative up float", value=-1.50000001, expected=-2),
    RoundHalfUpTestData(id="half_even", value=2.5, expected=3),
    RoundHalfUpTestData(id="half_even", value=3.5, expected=4),
]


@pytest.mark.parametrize("data", round_half_up_test_data, ids=lambda data: data.id)
def test_round_half_up(data: RoundHalfUpTestData) -> None:
    """Test for the utils.round_half_up function.

    Ensure the number passed is consistently rounded to the nearest
    integer with ties going away from zero.
    """
    result = utils.round_half_up(data.value)
    assert result == data.expected


def test_path_is_relative_to():
    """Ensure path_is_relative_to returns accurate results."""
    directory = Path("/tmp/test")
    file_in_directory = Path("/tmp/test/file.txt")
    assert utils.path_is_relative_to(child=file_in_directory, parent=directory)
    assert not utils.path_is_relative_to(child=directory, parent=file_in_directory)
