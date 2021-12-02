""" tests for the utilities in utils
"""
import os

from typing import List
from typing import Optional
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
    assert any((expected in exit_msg.message for exit_msg in exit_messages))


def test_find_many_settings_cwd(monkeypatch) -> None:
    """test more than one in cwd"""

    paths = [os.path.join(os.getcwd(), "ansible-navigator" + ext) for ext in EXTENTIONS]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    _messages, exit_messages, _found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any((expected in exit_msg.message for exit_msg in exit_messages))


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


@pytest.mark.parametrize(
    "value, anticpated_result",
    [(1, "1s"), (60 + 1, "1m1s"), (3600 + 60 + 1, "1h1m1s"), (86400 + 3600 + 60 + 1, "1d1h1m1s")],
    ids=["seconds", "minutes seconds", "hours minutes seconds", "days minutes seconds"],
)
def test_human_time(value: Union[int, float], anticpated_result: str) -> None:
    """test for human time"""
    # pass integer
    int_result = utils.human_time(value)
    assert int_result == anticpated_result
    # pass negative integer
    neg_int_result = utils.human_time(-value)
    assert neg_int_result == f"-{anticpated_result}"
    # pass float
    float_result = utils.human_time(float(value))
    assert float_result == anticpated_result
    # pass negative float
    neg_float_result = utils.human_time(-value)
    assert neg_float_result == f"-{anticpated_result}"
