""" tests for cli
"""
from copy import deepcopy
from unittest.mock import patch

import pytest

from ansible_navigator.cli import parse_and_update
from ansible_navigator.cli import NavigatorConfiguration

from ansible_navigator.configuration_subsystem import Constants as C

from ..defaults import FIXTURES_DIR


@pytest.mark.parametrize(
    "given, argname, expected",
    [
        (
            ["doc", "-t", "callback", "oneline"],
            "plugin_type",
            "callback",
        ),
        (
            ["doc", "sudo"],
            "plugin_name",
            "sudo",
        ),
        (
            ["doc", "-t", "become", "sudo"],
            "plugin_type",
            "become",
        ),
        (
            ["config"],
            "execution_environment_image",
            "quay.io/ansible/ansible-runner:devel",
        ),
        (
            ["config"],
            "log_level",
            "critical",
        ),
        (
            ["config", "--log-level", "debug"],
            "log_level",
            "debug",
        ),
        ([], "editor_command", "emacs -nw +{line_number} {filename}"),
        (
            ["inventory", "-i", "/tmp/inventory.yaml"],
            "inventory",
            ["/tmp/inventory.yaml"],
        ),
        (
            ["run", "site.yaml", "-i", "/tmp/inventory.yaml"],
            "inventory",
            ["/tmp/inventory.yaml"],
        ),
        (
            ["inventory", "-i", "/inv0.yaml", "-i", "/inv1.yaml"],
            "inventory",
            ["/inv0.yaml", "/inv1.yaml"],
        ),
        (
            ["run", "site.yaml", "-i", "/inv0.yaml", "-i", "/inv1.yaml"],
            "inventory",
            ["/inv0.yaml", "/inv1.yaml"],
        ),
        (
            ["run", "/site.yaml"],
            "playbook",
            "/site.yaml",
        ),
    ],
    ids=[
        "commandline overrides config file value",
        "config file overrides internal default value",
        "explicitly specifying the default still uses default",
        "internal default value gets picked if not overridden",
        "nested config option default",
        "nested config option override by commandline",
        "check editor command",
        "simple inventory test",
        "playbook with inventory",
        "multiple inventory",
        "run and multiple inventory",
        "run, check playbook",
    ],
)
# pylint:disable=redefined-outer-name
@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_update_args_general(_mf1, monkeypatch, given, argname, expected):
    """test the parse and update function"""

    monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", f"{FIXTURES_DIR}/unit/cli/ansible-navigator.yml")
    args = deepcopy(NavigatorConfiguration)
    _messages, errors = parse_and_update(params=given, args=args, initial=True)
    assert errors == []
    result = args.entry(argname)
    assert result.value.current == expected, result


@patch("distutils.spawn.find_executable", return_value="/path/to/container_engine")
def test_editor_command_default(_mf1, monkeypatch):
    """test editor with default"""
    monkeypatch.setenv(
        "ANSIBLE_NAVIGATOR_CONFIG", f"{FIXTURES_DIR}/unit/cli/ansible-navigator_empty.yml"
    )
    args = deepcopy(NavigatorConfiguration)
    _messages, errors = parse_and_update(params=[], args=args, initial=True)
    assert errors == []
    assert args.editor_command == "vi +{line_number} {filename}"
