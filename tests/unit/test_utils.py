""" tests for the utilities in utils
"""
import os
import pytest
import stat

from types import SimpleNamespace
from typing import List

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
    log_msg = "Skipping .ansible-navigator because required file ansible-navigator does not exist"
    assert log_msg in msgs
