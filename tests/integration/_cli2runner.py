"""Test from the CLI up to to the invocation of runner."""
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Dict

import pytest

from pytest_mock import MockerFixture


if TYPE_CHECKING:
    from unittest.mock import MagicMock  # pylint: disable=preferred-module


class RunnerTestException(Exception):
    """Custom exception for runner to throw."""


@pytest.mark.usefixtures("patch_curses")
class Cli2Runner:
    """A base class which mocks the runner calls."""

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

    cli_entry = "ansible-navigator {0} {1} -m {2}"

    def run_test(
        self,
        mocked_runner: "MagicMock",
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=no-self-use
        # pylint: disable=too-many-arguments
        """Confirm execution of ``cli.main()`` produces the desired results.

        :param mocked_runner: A patched instance of runner
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param cli_entry: The CLI entry to set as :data:`sys.argv`
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        :raises Exception: If called
        """
        raise Exception("Override in subclass")

    def test_config_interactive(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        """Test using config, interactive.

        :param mocker: The mocker fixture
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param comment: The test comment
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.ansible_config.get_ansible_config",
            side_effect=RunnerTestException,
        )
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_ALLOW_UI_TRACEBACK", "true")
        cli_entry = self.cli_entry.format(self.INTERACTIVE["config"], cli_entry, "interactive")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)

    def test_config_stdout(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        """Test using config, stdout.

        :param mocker: The mocker fixture
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param comment: The test comment
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command.run_command",
            side_effect=RunnerTestException,
        )
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_ALLOW_UI_TRACEBACK", "true")
        cli_entry = self.cli_entry.format(self.STDOUT["config"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)

    def test_inventory_interactive(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        """Test using inventory, interactive.

        :param mocker: The mocker fixture
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param comment: The test comment
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.ansible_inventory.get_inventory",
            side_effect=RunnerTestException,
        )
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_ALLOW_UI_TRACEBACK", "true")
        cli_entry = self.cli_entry.format(self.INTERACTIVE["inventory"], cli_entry, "interactive")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)

    def test_inventory_stdout(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        """Test using inventory, stdout.

        :param mocker: The mocker fixture
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param comment: The test comment
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command.run_command",
            side_effect=RunnerTestException,
        )
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_ALLOW_UI_TRACEBACK", "true")
        cli_entry = self.cli_entry.format(self.STDOUT["inventory"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)

    def test_run_interactive(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        """Test using run, interactive.

        :param mocker: The mocker fixture
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param comment: The test comment
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command_async.run_command_async",
            side_effect=RunnerTestException,
        )
        monkeypatch.setenv("ANSIBLE_NAVIGATOR_ALLOW_UI_TRACEBACK", "true")
        cli_entry = self.cli_entry.format(self.INTERACTIVE["run"], cli_entry, "interactive")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)

    def test_run_stdout(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: Dict[str, str],
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=unused-argument
        """Test using run, stdout.

        :param mocker: The mocker fixture
        :param monkeypatch: The monkeypatch fixture
        :param tmp_path: A test specific temporary path
        :param comment: The test comment
        :param cli_entry: The CLI entry to set as ``sys.argv``
        :param config_fixture: The settings fixture
        :param expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command_async.run_command_async",
            side_effect=RunnerTestException,
        )
        cli_entry = self.cli_entry.format(self.STDOUT["run"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)
