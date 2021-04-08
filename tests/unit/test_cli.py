""" tests for cli
"""
import os
import pytest

from ansible_navigator.cli import parse_and_update


@pytest.fixture
def test_fixtures_dir():
    """simple fixture for fixture directory"""
    return os.path.join(os.path.dirname(__file__), "..", "fixtures")


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
            "ee_image",
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
# pylint: disable=import-outside-toplevel
def test_update_args(mocker, test_fixtures_dir, given, argname, expected):
    """test the parse and update function"""
    mocker.patch("ansible_navigator.cli.get_conf_dir", return_value=(test_fixtures_dir, []))

    _pre_logger_msgs, args = parse_and_update(given)
    result = vars(args)[argname]
    assert result == expected


# pylint: disable=import-outside-toplevel
def test_editor_command_default(mocker):
    """test editor with defualt"""
    mocker.patch("ansible_navigator.cli.get_conf_dir", return_value=(None, []))

    _pre_logger_msgs, args = parse_and_update([])
    assert args.editor_command == "vi +{line_number} {filename}"
