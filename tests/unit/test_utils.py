""" tests for the utilities in utils
"""
import os
import pytest
import stat

from typing import List
from typing import Optional
from types import SimpleNamespace

import ansible_navigator.utils as utils


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


def test_get_conf_path_allowed_extension_failed(monkeypatch) -> None:
    """test get_conf_path"""

    def check_path_exists(arg):
        if arg in [
            "/etc/ansible-navigator/ansible-navigator.yaml",
            "/etc/ansible-navigator/ansible-navigator.yml",
            "/etc/ansible-navigator/ansible-navigator.json",
        ]:
            return True
        else:
            return False

    monkeypatch.setattr(os.path, "exists", check_path_exists)

    error_msg = (
        "only one file among 'ansible-navigator.json, ansible-navigator.yaml,"
        " ansible-navigator.yml' should be present under directory"
        " '/etc/ansible-navigator' instead multiple config files found"
        " '/etc/ansible-navigator/ansible-navigator.json,"
        " /etc/ansible-navigator/ansible-navigator.yaml,"
        " /etc/ansible-navigator/ansible-navigator.yml'"
    )
    with pytest.raises(SystemExit) as exc:
        assert utils.get_conf_path("ansible-navigator", allowed_extensions=["json", "yaml", "yml"])
        assert str(exc) == error_msg


def test_get_conf_path_allowed_extension_passed(monkeypatch) -> None:
    """test get_conf_path"""

    expected_config_file_path = os.path.expanduser(
        "~/.config/ansible-navigator/ansible-navigator.yaml"
    )

    def check_path_exists(arg):
        if arg == expected_config_file_path:
            return True
        else:
            return False

    def get_dir_permission(arg):
        if arg == os.path.dirname(expected_config_file_path):
            return SimpleNamespace(**{"st_mode": stat.S_IROTH})

    monkeypatch.setattr(os.path, "exists", check_path_exists)
    monkeypatch.setattr(os, "stat", get_dir_permission)

    received_config_file_path, msgs = utils.get_conf_path(
        "ansible-navigator", allowed_extensions=["json", "yaml", "yml"]
    )

    assert received_config_file_path == expected_config_file_path
    log_msg = "Skipping .ansible-navigator/ansible-navigator.json because it does not exist"
    assert log_msg in msgs


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
    result = utils.env_var_is_file_path(envvar, "config")
    assert result[0] == anticpated_result
