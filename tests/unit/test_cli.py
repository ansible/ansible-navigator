"""Tests using the CLi directly."""

import shlex

from copy import deepcopy
from pathlib import Path
from typing import Any
from typing import Literal
from typing import NamedTuple

# pylint: disable=preferred-module
from unittest.mock import patch

import pytest

from ansible_navigator.cli import NavigatorConfiguration
from ansible_navigator.cli import main
from ansible_navigator.initialization import parse_and_update
from tests.defaults import FIXTURES_DIR


@pytest.mark.parametrize(
    ("given", "argname", "expected"),
    (
        pytest.param(
            ["doc", "-t", "callback", "oneline"],
            "plugin_type",
            "callback",
            id="commandline-overrides-config-file-value",
        ),
        pytest.param(
            ["doc", "sudo"],
            "plugin_name",
            "sudo",
            id="config-file-overrides-internal-default-value",
        ),
        pytest.param(
            ["doc", "-t", "become", "sudo"],
            "plugin_type",
            "become",
            id="explicitly-specifying-the-default-still-uses-default",
        ),
        pytest.param(
            ["config"],
            "execution_environment_image",
            "ghcr.io/ansible/community-ansible-dev-tools:latest",
            id="internal-default-value-gets-picked-if-not-overridden",
        ),
        pytest.param(
            ["config"],
            "log_level",
            "critical",
            id="nested-config-option-default",
        ),
        pytest.param(
            ["config", "--log-level", "debug"],
            "log_level",
            "debug",
            id="nested-config-option-override-by-commandline",
        ),
        pytest.param(
            [],
            "editor_command",
            "emacs -nw +{line_number} {filename}",
            id="check-editor-command",
        ),
        pytest.param(
            ["inventory", "-i", "/tmp/inventory.yaml"],
            "inventory",
            ["/tmp/inventory.yaml"],
            id="simple-inventory-test",
        ),
        pytest.param(
            ["run", "site.yaml", "-i", "/tmp/inventory.yaml"],
            "inventory",
            ["/tmp/inventory.yaml"],
            id="playbook-with-inventory",
        ),
        pytest.param(
            ["inventory", "-i", "/inv0.yaml", "-i", "/inv1.yaml"],
            "inventory",
            ["/inv0.yaml", "/inv1.yaml"],
            id="multiple-inventory",
        ),
        pytest.param(
            ["run", "site.yaml", "-i", "/inv0.yaml", "-i", "/inv1.yaml"],
            "inventory",
            ["/inv0.yaml", "/inv1.yaml"],
            id="run-and-multiple-inventory",
        ),
        pytest.param(
            ["run", "/site.yaml"],
            "playbook",
            "/site.yaml",
            id="run-check-playbook",
        ),
        pytest.param(
            ["run", "/site.yaml", "--", "-e", "foo=bar"],
            "playbook",
            "/site.yaml",
            id="run-check-with-extra-parameters-1",
        ),
        pytest.param(
            ["run", "/site.yaml", "--", "-e", "foo=bar"],
            "cmdline",
            ["-e", "foo=bar"],
            id="run-check-with-extra-parameters-2",
        ),
    ),
)
@patch("shutil.which", return_value="/path/to/container_engine")
def test_update_args_general(
    _mf1: Any,
    monkeypatch: pytest.MonkeyPatch,
    given: list[str],
    argname: Literal[
        "plugin_type",
        "plugin_name",
        "execution_environment_image",
        "log_level",
        "editor_command",
        "inventory",
        "playbook",
        "cmdline",
    ],
    expected: list[str],
) -> None:
    """Test the parse and update function.

    Args:
        monkeypatch: The monkeypatch fixture
        given: Exit message params
        argname: Name of the entry
        expected: Expected value of the entry
    """
    monkeypatch.setenv("ANSIBLE_NAVIGATOR_CONFIG", f"{FIXTURES_DIR}/unit/cli/ansible-navigator.yml")
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    args.application_version = "test"
    _messages, exit_msgs = parse_and_update(params=given, args=args)
    assert not exit_msgs
    result = args.entry(argname)
    assert result.value.current == expected, result


@patch("shutil.which", return_value="/path/to/container_engine")
def test_editor_command_default(_mf1: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test editor with default.

    Args:
        monkeypatch: The monkeypatch fixture
    """
    monkeypatch.setenv(
        "ANSIBLE_NAVIGATOR_CONFIG",
        f"{FIXTURES_DIR}/unit/cli/ansible-navigator_empty.yml",
    )
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    args.application_version = "test"
    _messages, exit_msgs = parse_and_update(params=[], args=args)
    assert not exit_msgs
    assert args.editor_command == "vi +{line_number} {filename}"


class TstHint(NamedTuple):
    """Obj for hint test data."""

    command: str
    expected: str
    prefix: str = "Try again"
    set_ce: bool = False


tst_hint_data = [
    pytest.param(
        TstHint(
            command=r"--cdcp {locked_directory}/foo.db",
            expected="without '--cdcp'",
            set_ce=True,
        ),
        id="0",
    ),
    pytest.param(TstHint(command="--econ not_bool", expected="with '--econ true'"), id="1"),
    pytest.param(TstHint(command="--ee not_bool", expected="with '--ee true'"), id="2"),
    pytest.param(TstHint(command="inventory", expected="with '-i <path to inventory>'"), id="3"),
    pytest.param(TstHint(command="--la not_bool", expected="with '--la true'"), id="4"),
    pytest.param(
        TstHint(
            command="--lf {locked_directory}/test.log",
            expected="with '--lf ~/ansible-navigator.log'",
        ),
        id="5",
    ),
    pytest.param(TstHint(command="-m stderr", expected="with '-m stdout'"), id="6"),
    pytest.param(TstHint(command="--osc4 not_bool", expected="with '--osc4 true'"), id="7"),
    pytest.param(TstHint(command="doc", expected="with 'doc <plugin_name>"), id="8"),
    pytest.param(TstHint(command="run", expected="with 'run <playbook name>"), id="9"),
    pytest.param(TstHint(command="run --pae not_bool", expected="with '--pae true"), id="10"),
    pytest.param(
        TstHint(command="replay", expected="with 'replay <path to playbook artifact>'"),
        id="11",
    ),
    pytest.param(
        TstHint(command="--senv FOO:BAR", expected="with '--senv MY_VAR=my_value'"),
        id="12",
    ),
]


@pytest.mark.parametrize("data", tst_hint_data)
def test_hints(
    monkeypatch: pytest.MonkeyPatch,
    locked_directory: str,
    valid_container_engine: str,
    data: TstHint,
) -> None:
    """Test the hints don't generate a traceback.

    Args:
        monkeypatch: The monkeypatch fixture
        locked_directory: Locked directory
        valid_container_engine: Container engine
        data: Test object
    """
    monkeypatch.setenv(
        "ANSIBLE_NAVIGATOR_CONFIG",
        f"{FIXTURES_DIR}/unit/cli/ansible-navigator_empty.yml",
    )
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    args.application_version = "test"
    command = data.command.format(locked_directory=locked_directory)
    params = shlex.split(command)
    if data.set_ce:
        params += ["--ce", valid_container_engine]

    _messages, exit_msgs_obj = parse_and_update(params=params, args=args)
    expected = f"{data.prefix} {data.expected}"
    exit_msgs = [exit_msg.message for exit_msg in exit_msgs_obj]
    assert any(expected in exit_msg for exit_msg in exit_msgs), (expected, exit_msgs)


def test_no_term(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test for err and hint w/o TERM.

    Args:
        monkeypatch: The monkeypatch fixture
    """
    monkeypatch.delenv("TERM")
    args = deepcopy(NavigatorConfiguration)
    args.internals.initializing = True
    params: list[str] = []
    _messages, exit_msgs_obj = parse_and_update(params=params, args=args)
    exit_msgs = [exit_msg.message for exit_msg in exit_msgs_obj]
    expected = "TERM environment variable must be set"
    assert any(expected in exit_msg for exit_msg in exit_msgs), (expected, exit_msgs)
    expected = "Try again after setting the TERM environment variable"
    assert any(expected in exit_msg for exit_msg in exit_msgs), (expected, exit_msgs)


def test_for_version_logged(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    tmp_path: Path,
) -> None:
    """Ensure the version is captured in the log.

    Args:
        monkeypatch: The monkey patch fixture
        caplog: The log capture fixture
        tmp_path: A temporary director for this test
    """
    logfile = tmp_path / "log.txt"
    command_line = [
        "ansible-navigator",
        "exec",
        "ls",
        "--ll",
        "debug",
        "--lf",
        str(logfile),
        "--pp",
        "never",
    ]
    monkeypatch.setattr("sys.argv", command_line)
    with pytest.raises(SystemExit):
        # A SystemExit happens here because the container vanishes quickly
        main()
    assert "ansible-navigator==" in caplog.text
    assert "ansible-runner==" in caplog.text
