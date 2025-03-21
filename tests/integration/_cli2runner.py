"""Test from the CLI up to to the invocation of runner."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from pathlib import Path
    from unittest.mock import MagicMock  # pylint: disable=preferred-module

    from pytest_mock import MockerFixture


class RunnerTestError(Exception):
    """Custom exception for runner to throw."""


@pytest.mark.usefixtures("_patch_curses")
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
        mocked_runner: MagicMock,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        cli_entry: str,
        config_fixture: str,
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Confirm execution of ``cli.main()`` produces the desired results.

        Args:
            mocked_runner: A patched instance of runner
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            cli_entry: The CLI entry to set as :data:`sys.argv`
            config_fixture: The settings fixture
            expected: the expected return value
        """
        pytest.exit(reason="Override in subclass", returncode=1)

    def test_config_interactive(
        self,
        mocker: MockerFixture,
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path,
        comment: str,
        cli_entry: str,
        config_fixture: str,
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Test using config, interactive.

        Args:
            mocker: The mocker fixture
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            comment: The test comment
            cli_entry: The CLI entry to set as ``sys.argv``
            config_fixture: The settings fixture
            expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.ansible_config.get_ansible_config",
            side_effect=RunnerTestError,
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
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Test using config, stdout.

        Args:
            mocker: The mocker fixture
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            comment: The test comment
            cli_entry: The CLI entry to set as ``sys.argv``
            config_fixture: The settings fixture
            expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command.run_command",
            side_effect=RunnerTestError,
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
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Test using inventory, interactive.

        Args:
            mocker: The mocker fixture
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            comment: The test comment
            cli_entry: The CLI entry to set as ``sys.argv``
            config_fixture: The settings fixture
            expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.ansible_inventory.get_inventory",
            side_effect=RunnerTestError,
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
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Test using inventory, stdout.

        Args:
            mocker: The mocker fixture
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            comment: The test comment
            cli_entry: The CLI entry to set as ``sys.argv``
            config_fixture: The settings fixture
            expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command.run_command",
            side_effect=RunnerTestError,
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
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Test using run, interactive.

        Args:
            mocker: The mocker fixture
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            comment: The test comment
            cli_entry: The CLI entry to set as ``sys.argv``
            config_fixture: The settings fixture
            expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command_async.run_command_async",
            side_effect=RunnerTestError,
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
        expected: dict[str, str],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Test using run, stdout.

        Args:
            mocker: The mocker fixture
            monkeypatch: The monkeypatch fixture
            tmp_path: A test specific temporary path
            comment: The test comment
            cli_entry: The CLI entry to set as ``sys.argv``
            config_fixture: The settings fixture
            expected: the expected return value
        """
        mocked_runner = mocker.patch(
            target="ansible_navigator.runner.command_async.run_command_async",
            side_effect=RunnerTestError,
        )
        cli_entry = self.cli_entry.format(self.STDOUT["run"], cli_entry, "stdout")
        self.run_test(mocked_runner, monkeypatch, tmp_path, cli_entry, config_fixture, expected)
