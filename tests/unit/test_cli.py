""" tests for cli
"""
import pytest

import ansible_navigator.cli as cli

from ..defaults import FIXTURES_DIR


@pytest.mark.parametrize(
    "given, argname, expected",
    [
        (
            ["doc", "-t", "callback", "oneline"],
            "type",
            "callback",
        ),
        (
            ["doc", "sudo"],
            "type",
            "become",
        ),
        (
            ["doc", "-t", "become", "sudo"],
            "type",
            "become",
        ),
        (
            ["config"],
            "execution_environment_image",
            "quay.io/ansible/ansible-runner:devel",
        ),
        (
            ["config"],
            "loglevel",
            "critical",
        ),
        (
            ["config", "--loglevel", "debug"],
            "loglevel",
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
def test_update_args_general(monkeypatch, given, argname, expected):
    """test the parse and update function"""

    monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", f"{FIXTURES_DIR}/unit/cli/ansible-navigator.yml")
    _pre_logger_msgs, args = cli.parse_and_update(given)
    result = vars(args)[argname]
    assert result == expected


def test_editor_command_default(monkeypatch):
    """test editor with default"""
    monkeypatch.setenv(
        "ANSIBLE_NAVIGATOR_CONFIG", f"{FIXTURES_DIR}/unit/cli/ansible-navigator_empty.yml"
    )
    _pre_logger_msgs, args = cli.parse_and_update([])
    assert args.editor_command == "vi +{line_number} {filename}"
