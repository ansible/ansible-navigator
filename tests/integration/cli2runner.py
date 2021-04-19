""" a base class to test from the cli to runner
requires a data struct of
comment, cli_entry, config_fixture, expected
"""

import curses
import logging

from unittest import mock

import pytest

from ..defaults import FIXTURES_DIR


class Cli2Runner:
    # pylint: disable=unused-argument
    # pylint: disable=attribute-defined-outside-init
    # pylint: disable= redefined-outer-name
    # pylint: disable=too-many-arguments
    # pylint: disable=no-member
    """a base class to test from the cli to runner
    requires a data struct of
    comment, cli_entry, config_fixture, expected
    in a parameterize decorator for the subclass
    """

    TEST_FIXTURE_DIR = f"{FIXTURES_DIR}/integration/SET_IN_SUBCLASS"

    STDOUT = {
        "config": "SET_IN_SUBCLASS",
        "inventory": "SET_IN_SUBCLASS",
        "run": "SET_IN_SUBCLASS",
    }

    INTERACTIVE = {
        "config": "SET_IN_SUBCLASS",
        "inventory": "SET_IN_SUBCLASS",
        "run": "SET_IN_SUBCLASS",
    }

    def run_test(self, mocked_runner, cli_entry, config_fixture, expected):
        # pylint: disable=no-self-use
        """called by every test
        override in subclass
        """
        raise Exception("override me in subclass")

    @staticmethod
    @pytest.fixture
    def patch_curses(monkeypatch):
        """patch curses so it doesn't Traceback during tests"""
        # pylint: disable=import-outside-toplevel
        monkeypatch.setattr(curses, "cbreak", lambda: None)
        monkeypatch.setattr(curses, "nocbreak", lambda: None)
        monkeypatch.setattr(curses, "endwin", lambda: None)

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.cli_entry = "ansible-navigator {0} {1} -m {2}"

    @mock.patch("ansible_navigator.runner.api.get_ansible_config")
    def test_config_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["config"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command")
    def test_config_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["config"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.get_inventory")
    def test_inventory_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["inventory"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command")
    def test_inventory_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["inventory"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command_async")
    def test_run_interactive(
        self, mocked_runner, comment, cli_entry, config_fixture, expected, patch_curses
    ):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.INTERACTIVE["run"], cli_entry, "interactive")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)

    @mock.patch("ansible_navigator.runner.api.run_command_async")
    def test_run_stdout(self, mocked_runner, comment, cli_entry, config_fixture, expected):
        # pylint: disable=unused-argument
        """test use of set_environment_variable"""
        cli_entry = self.cli_entry.format(self.STDOUT["run"], cli_entry, "stdout")
        self.run_test(mocked_runner, cli_entry, config_fixture, expected)
