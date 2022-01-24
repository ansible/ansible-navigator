"""tests for CLI
"""
import shlex

from copy import deepcopy
from typing import NamedTuple
from unittest.mock import patch

import pytest

from ansible_navigator.cli import NavigatorConfiguration
from ansible_navigator.cli import parse_and_update
from ..defaults import FIXTURES_DIR


@pytest.mark.parametrize(
    "given, argname, expected",
    (
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
            "quay.io/ansible/creator-ee:v0.2.0",
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
    ),
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
@patch("shutil.which", return_value="/path/to/container_engine")
def test_update_args_general(_mf1, monkeypatch, given, argname, expected):
    """test the parse and update function"""

    monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", f"{FIXTURES_DIR}/unit/cli/ansible-navigator.yml")
    args = deepcopy(NavigatorConfiguration)
    _messages, exit_msgs = parse_and_update(params=given, args=args, initial=True)
    assert not exit_msgs
    result = args.entry(argname)
    assert result.value.current == expected, result


@patch("shutil.which", return_value="/path/to/container_engine")
def test_editor_command_default(_mf1, monkeypatch):
    """test editor with default"""
    monkeypatch.setenv(
        "ANSIBLE_NAVIGATOR_CONFIG",
        f"{FIXTURES_DIR}/unit/cli/ansible-navigator_empty.yml",
    )
    args = deepcopy(NavigatorConfiguration)
    _messages, exit_msgs = parse_and_update(params=[], args=args, initial=True)
    assert not exit_msgs
    assert args.editor_command == "vi +{line_number} {filename}"


def id_for_hint_test(value):
    """generate an id for the hint test
    the spaces here help with zsh
    https://github.com/microsoft/vscode-python/issues/10398
    """
    return f" {value.command} "


class TstHint(NamedTuple):
    """obj for hint test data"""

    command: str
    expected: str
    prefix: str = "Try again"
    set_ce: bool = False


tst_hint_data = [
    TstHint(command=r"--cdcp {locked_directory}/foo.db", expected="without '--cdcp'", set_ce=True),
    TstHint(command="--econ troo", expected="with '--econ true'"),
    TstHint(command="--ee troo", expected="with '--ee true'"),
    TstHint(command="config --help-config --mode interactive", expected="with '-m stdout'"),
    TstHint(command="doc --help-doc --mode interactive", expected="with '-m stdout'"),
    TstHint(command="inventory", expected="with '-i <path to inventory>'"),
    TstHint(command="--la fallss", expected="with '--la true'"),
    TstHint(
        command="--lf {locked_directory}/test.log",
        expected="with '--lf ~/ansible-navigator.log'",
    ),
    TstHint(command="-m stderr", expected="with '-m stdout'"),
    TstHint(command="--osc4 troo", expected="with '--osc4 true'"),
    TstHint(command="doc", expected="with 'doc <plugin_name>"),
    TstHint(command="run", expected="with 'run <playbook name>"),
    TstHint(command="run --pae troo", expected="with '--pae true"),
    TstHint(command="replay", expected="with 'replay <path to playbook artifact>'"),
    TstHint(command="--senv FOO:BAR", expected="with '--senv MYVAR=myvalue'"),
]


@pytest.mark.parametrize("data", tst_hint_data, ids=id_for_hint_test)
def test_hints(monkeypatch, locked_directory, valid_container_engine, data):
    """test the hints don't generate a traceback"""
    monkeypatch.setenv(
        "ANSIBLE_NAVIGATOR_CONFIG",
        f"{FIXTURES_DIR}/unit/cli/ansible-navigator_empty.yml",
    )
    args = deepcopy(NavigatorConfiguration)
    command = data.command.format(locked_directory=locked_directory)
    params = shlex.split(command)
    if data.set_ce:
        params += ["--ce", valid_container_engine]

    _messages, exit_msgs = parse_and_update(params=params, args=args, initial=True)
    expected = f"{data.prefix} {data.expected}"
    exit_msgs = [exit_msg.message for exit_msg in exit_msgs]
    assert any(expected in exit_msg for exit_msg in exit_msgs), (expected, exit_msgs)


def test_no_term(monkeypatch):
    """test for err and hint w/o TERM"""
    monkeypatch.delenv("TERM")
    args = deepcopy(NavigatorConfiguration)
    params = []
    _messages, exit_msgs = parse_and_update(params=params, args=args, initial=True)
    exit_msgs = [exit_msg.message for exit_msg in exit_msgs]
    expected = "TERM environment variable must be set"
    assert any(expected in exit_msg for exit_msg in exit_msgs), (expected, exit_msgs)
    expected = "Try again after setting the TERM environment variable"
    assert any(expected in exit_msg for exit_msg in exit_msgs), (expected, exit_msgs)
