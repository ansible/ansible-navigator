""" tests for the utilities in utils
"""
import os
import stat

from typing import List
from typing import Optional
from types import SimpleNamespace

import pytest

import ansible_navigator.utils as utils

EXTENTIONS = [".yml", ".yaml", ".json"]


def test_find_many_settings_home(monkeypatch) -> None:
    """test more than one in home"""

    paths = [
        os.path.join(os.path.expanduser("~"), ".ansible-navigator" + ext) for ext in EXTENTIONS
    ]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    messages, exit_messages, found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any([expected in exit_msg.message for exit_msg in exit_messages])


def test_find_many_settings_cwd(monkeypatch) -> None:
    """test more than one in cwd"""

    paths = [os.path.join(os.getcwd(), "ansible-navigator" + ext) for ext in EXTENTIONS]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    messages, exit_messages, found = utils.find_settings_file()
    expected = f"Only one file among {utils.oxfordcomma(paths, 'and')}"
    assert any([expected in exit_msg.message for exit_msg in exit_messages])


def test_find_many_settings_precedence(monkeypatch) -> None:
    """test more than one in cwd"""

    expected = os.path.join(os.getcwd(), "ansible-navigator.yml")
    paths = [expected, os.path.join(os.path.expanduser("~"), ".ansible-navigator.json")]

    def check_path_exists(arg):
        return arg in paths

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    messages, exit_messages, found = utils.find_settings_file()
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
