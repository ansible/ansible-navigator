""" test the use of set_environment_variable throguh to runner
"""
import os

from unittest import mock

import pytest

import ansible_navigator.cli as cli

from ..defaults import FIXTURES_DIR

test_data = [
    ("not set", "", "ansible-navigator_empty.yml", {}),
    (
        "set 1 at command line",
        "--penv TEST_ENV0",
        "ansible-navigator_empty.yml",
        {"TEST_ENV0": "te0"},
    ),
    (
        "set 2 at command line",
        "--penv TEST_ENV0 --penv TEST_ENV1",
        "ansible-navigator_empty.yml",
        {"TEST_ENV0": "te0", "TEST_ENV1": "te1"},
    ),
    (
        "set 3 in config file",
        "",
        "ansible-navigator.yml",
        {"TEST_ENV0": "te0", "TEST_ENV1": "te1", "TEST_ENV2": "te2"},
    ),
    (
        "set command line and config file, command line wins",
        "--penv TEST_ENV0",
        "ansible-navigator.yml",
        {"TEST_ENV0": "te0"},
    ),
]

run_commands = [
    "config dump",
    "inventory -i test_inventory",
]

run_async_commands = ["run site.yaml"]


@mock.patch("ansible_navigator.runner.api.run_command")
@pytest.mark.parametrize(
    argnames=("comment", "cli_entry", "config_fixture", "expected"),
    argvalues=test_data,
    ids=[f"{idx}: {i[0]}" for idx, i in enumerate(test_data)],
)
@pytest.mark.parametrize(
    argnames="command",
    argvalues=run_commands,
    ids=[cmd.split()[0] for cmd in run_commands],
)
def test_w_run_command(mocked_runner, command, comment, cli_entry, config_fixture, expected):
    # pylint: disable=unused-argument
    """test use of set_environment_variable"""
    mocked_runner.side_effect = Exception("called")
    cli_entry = f"ansible-navigator {command} {cli_entry} -m stdout"
    with mock.patch("sys.argv", cli_entry.split()):
        cfg_path = f"{FIXTURES_DIR}/{config_fixture}"
        with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_CONFIG": cfg_path}):
            with mock.patch.dict(os.environ, expected):
                with pytest.raises(Exception, match="called"):
                    cli.main()

    _args, kwargs = mocked_runner.call_args
    for item in expected.items():
        assert item in kwargs["envvars"].items()


@mock.patch("ansible_navigator.runner.api.run_command_async")
@pytest.mark.parametrize(
    argnames=("comment", "cli_entry", "config_fixture", "expected"),
    argvalues=test_data,
    ids=[f"{idx}: {i[0]}" for idx, i in enumerate(test_data)],
)
@pytest.mark.parametrize(
    argnames="command",
    argvalues=run_async_commands,
    ids=[cmd.split()[0] for cmd in run_async_commands],
)
def test_w_run_command_async(mocked_runner, command, comment, cli_entry, config_fixture, expected):
    # pylint: disable=unused-argument
    """test use of set_environment_variable"""
    mocked_runner.side_effect = Exception("called")
    cli_entry = f"ansible-navigator {command} {cli_entry} -m stdout"
    with mock.patch("sys.argv", cli_entry.split()):
        cfg_path = f"{FIXTURES_DIR}/{config_fixture}"
        with mock.patch.dict(os.environ, {"ANSIBLE_NAVIGATOR_CONFIG": cfg_path}):
            with mock.patch.dict(os.environ, expected):
                with pytest.raises(Exception, match="called"):
                    cli.main()

    _args, kwargs = mocked_runner.call_args
    for item in expected.items():
        assert item in kwargs["envvars"].items()
