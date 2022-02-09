"""test from CLI up to runner
"""
# pylint: disable=preferred-module  # FIXME: remove once migrated per GH-872
from unittest import mock

import pytest


class Cli2Runner:
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable=too-many-arguments
    # pylint: disable=unused-argument
    """A base class which mocks the runner calls"""

    INTERACTIVE = {
        "config": "override in subclass",
        "inventory": "override in subclass",
        "run": "override in subclass",
    }

    STDOUT = {
        "config": "override in subclass",
        "inventory": "override in subclass",
        "run": "override in subclass",
    }

    def run_test(self, mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected):
        # pylint: disable=no-self-use
        """Confirm execution of ``cli.main()`` produces the desired results.

        :param mocked_runner: A patched instance of runner
        :param monkeypatch: The monkey patch fixture
        :param tmpdir: A fixture generating a unique temporary directory
        :param cli_entry: The CLI entry to set as :data:`sys.argv`
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        raise Exception("Override in subclass")

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.cli_entry = "ansible-navigator {0} {1} -m {2}"

    @mock.patch("ansible_navigator.runner.ansible_config.get_ansible_config")
    def test_config_interactive(
        self,
        mocked_runner,
        monkeypatch,
        tmpdir,
        comment,
        cli_entry,
        config_fixture,
        expected,
        patch_curses,
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["config"], cli_entry, "interactive")
        self.run_test(mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.command.run_command")
    def test_config_stdout(
        self,
        mocked_runner,
        monkeypatch,
        tmpdir,
        comment,
        cli_entry,
        config_fixture,
        expected,
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["config"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.ansible_inventory.get_inventory")
    def test_inventory_interactive(
        self,
        mocked_runner,
        monkeypatch,
        tmpdir,
        comment,
        cli_entry,
        config_fixture,
        expected,
        patch_curses,
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["inventory"], cli_entry, "interactive")
        self.run_test(mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.command.run_command")
    def test_inventory_stdout(
        self,
        mocked_runner,
        monkeypatch,
        tmpdir,
        comment,
        cli_entry,
        config_fixture,
        expected,
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["inventory"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.command_async.run_command_async")
    def test_run_interactive(
        self,
        mocked_runner,
        monkeypatch,
        tmpdir,
        comment,
        cli_entry,
        config_fixture,
        expected,
        patch_curses,
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["run"], cli_entry, "interactive")
        self.run_test(mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.command_async.run_command_async")
    def test_run_stdout(
        self,
        mocked_runner,
        monkeypatch,
        tmpdir,
        comment,
        cli_entry,
        config_fixture,
        expected,
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["run"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmpdir, cli_entry, config_fixture, expected)
