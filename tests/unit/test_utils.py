""" tests for the utilities in utils
"""
import os

from typing import List
from typing import Optional
from typing import NamedTuple
from typing import Union

import pytest

from ansible_navigator import utils

EXTENTIONS = [".yml", ".yaml", ".json"]


def test_find_many_settings_home(monkeypatch) -> None:
    """test more than one in home"""

    paths = [
        os.path.join(os.path.expanduser("~"), ".ansible-navigator" + ext) for ext in EXTENTIONS
    ]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, exit_messages, _found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any(expected in exit_msg.message for exit_msg in exit_messages)


def test_find_many_settings_cwd(monkeypatch) -> None:
    """test more than one in cwd"""

    paths = [os.path.join(os.getcwd(), "ansible-navigator" + ext) for ext in EXTENTIONS]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, exit_messages, _found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any(expected in exit_msg.message for exit_msg in exit_messages)


def test_find_many_settings_precedence(monkeypatch) -> None:
    """test more than one in cwd"""

    expected = os.path.join(os.getcwd(), "ansible-navigator.yml")
    paths = [expected, os.path.join(os.path.expanduser("~"), ".ansible-navigator.json")]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, _exit_messages, found = utils.find_settings_file()
    assert expected == found


@pytest.mark.parametrize(
    "set_env, file_path, anticpated_result",
    [
        (True, os.path.abspath(__file__), os.path.abspath(__file__)),
        (True, "", None),
        (False, None, None),
    ],
    ids=[
        "set and valid",
        "set and invalid",
        "not set",
    ],
)
def test_env_var_is_file_path(
    monkeypatch, set_env: bool, file_path: str, anticpated_result: Optional[str]
) -> None:
    """test env var is a file path"""
    envvar = "ANSIBLE_NAVIGATOR_CONFIG"
    if set_env:
        monkeypatch.setenv(envvar, file_path)
    _messages, _exit_messages, result = utils.environment_variable_is_file_path(envvar, "config")
    assert result == anticpated_result


@pytest.mark.parametrize(
    "value, anticpated_result",
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, [3]], [1, 2, 3]),
        ([1, [2], [3, 4], 5, True, {6: False}], [1, 2, 3, 4, 5, True, {6: False}]),
    ],
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
    """data for human time test"""

    id: str
    value: Union[int, float]
    expected: str


human_time_test_data = [
    HumanTimeTestData(id="seconds", value=1, expected="1s"),
    HumanTimeTestData(id="minutes seconds", value=60 + 1, expected="1m1s"),
    HumanTimeTestData(id="hours minutes seconds", value=3600 + 60 + 1, expected="1h1m1s"),
    HumanTimeTestData(
        id="days hours minutes seconds", value=86400 + 3600 + 60 + 1, expected="1d1h1m1s"
    ),
]


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_integer(data: List) -> None:
    """test for the utils.human_time function (integer passed)"""
    result = utils.human_time(data.value)
    assert result == data.expected


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_negative_integer(data: List) -> None:
    """test for the utils.human_time function (negative integer passed)"""
    result = utils.human_time(-data.value)
    assert result == f"-{data.expected}"


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_float(data: List) -> None:
    """test for the utils.human_time function (float passed)"""
    result = utils.human_time(float(data.value))
    assert result == data.expected


@pytest.mark.parametrize("data", human_time_test_data, ids=lambda data: data.id)
def test_human_time_negative_float(data: List) -> None:
    """test for the utils.human_time function (negative float passed)"""
    result = utils.human_time(-float(data.value))
    assert result == f"-{data.expected}"
