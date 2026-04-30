"""Tests for the command runner module."""

from __future__ import annotations

import subprocess

from unittest.mock import MagicMock
from unittest.mock import patch

from ansible_navigator.command_runner.command_runner import Command
from ansible_navigator.command_runner.command_runner import CommandRunner
from ansible_navigator.command_runner.command_runner import run_command


def _noop(cmd: Command) -> None:
    """No-op post processor."""


class TestCommand:
    """Tests for the Command dataclass."""

    def test_default_values(self) -> None:
        """Test Command default values."""
        cmd = Command(identity="test", command="echo hi", post_process=_noop)
        assert cmd.return_code == 0
        assert cmd.stdout == ""
        assert cmd.stderr == ""
        assert cmd.details == []
        assert cmd.errors == ""
        assert cmd.messages == []

    def test_stdout_lines(self) -> None:
        """Test stdout_lines property."""
        cmd = Command(identity="t", command="t", post_process=_noop)
        cmd.stdout = "line1\nline2\nline3"
        assert cmd.stdout_lines == ["line1", "line2", "line3"]

    def test_stdout_lines_empty(self) -> None:
        """Test stdout_lines with empty stdout."""
        cmd = Command(identity="t", command="t", post_process=_noop)
        assert cmd.stdout_lines == []

    def test_stderr_lines(self) -> None:
        """Test stderr_lines property."""
        cmd = Command(identity="t", command="t", post_process=_noop)
        cmd.stderr = "err1\nerr2"
        assert cmd.stderr_lines == ["err1", "err2"]

    def test_stderr_lines_empty(self) -> None:
        """Test stderr_lines with empty stderr."""
        cmd = Command(identity="t", command="t", post_process=_noop)
        assert cmd.stderr_lines == []

    def test_is_mutable(self) -> None:
        """Test Command is mutable (frozen=False)."""
        cmd = Command(identity="t", command="t", post_process=_noop)
        cmd.return_code = 1
        cmd.stdout = "out"
        cmd.stderr = "err"
        assert cmd.return_code == 1


class TestRunCommand:
    """Tests for the run_command function."""

    @patch("ansible_navigator.command_runner.command_runner.subprocess.run")
    def test_success(self, mock_run: MagicMock) -> None:
        """Test run_command with successful execution."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "hello\n"
        mock_run.return_value = mock_result

        cmd = Command(identity="t", command="echo hello", post_process=_noop)
        run_command(cmd)

        assert cmd.return_code == 0
        assert cmd.stdout == "hello\n"
        assert cmd.stderr == ""

    @patch("ansible_navigator.command_runner.command_runner.subprocess.run")
    def test_failure(self, mock_run: MagicMock) -> None:
        """Test run_command with CalledProcessError."""
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="false",
            output="out",
            stderr="err",
        )

        cmd = Command(identity="t", command="false", post_process=_noop)
        run_command(cmd)

        assert cmd.return_code == 1
        assert cmd.stdout == "out"
        assert cmd.stderr == "err"


class TestCommandRunner:
    """Tests for the CommandRunner class."""

    def test_init(self) -> None:
        """Test CommandRunner initialization."""
        runner = CommandRunner()
        assert runner._completed_queue is None
        assert runner._pending_queue is None

    @patch("ansible_navigator.command_runner.command_runner.subprocess.run")
    def test_run_single_process(self, mock_run: MagicMock) -> None:
        """Test run_single_process executes and post-processes."""
        mock_run.return_value = MagicMock(returncode=0, stdout="out")
        calls: list[str] = []

        def track(cmd: Command) -> None:
            calls.append(cmd.identity)

        cmds = [
            Command(identity="a", command="echo a", post_process=track),
            Command(identity="b", command="echo b", post_process=track),
        ]

        results = CommandRunner.run_single_process(cmds)
        assert len(results) == 2
        assert calls == ["a", "b"]

    @patch("ansible_navigator.command_runner.command_runner.subprocess.run")
    def test_run_single_process_with_failure(self, mock_run: MagicMock) -> None:
        """Test run_single_process continues after failure."""
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="ok"),
            subprocess.CalledProcessError(1, "fail", output="", stderr="error"),
        ]

        cmds = [
            Command(identity="ok", command="echo ok", post_process=_noop),
            Command(identity="fail", command="false", post_process=_noop),
        ]

        results = CommandRunner.run_single_process(cmds)
        assert results[0].return_code == 0
        assert results[1].return_code == 1
