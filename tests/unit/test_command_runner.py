"""Unit tests for CommandRunner deadlock prevention."""

from __future__ import annotations

import multiprocessing
import queue

from types import SimpleNamespace

import pytest

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner import CommandRunner


def _noop_post_process(command: Command) -> None:
    command.details = {"status": "ok"}


def _crashing_post_process(command: Command) -> None:
    msg = f"Simulated crash in post_process for {command.identity}"
    raise RuntimeError(msg)


class TestRunMultiProcess:
    """Tests for CommandRunner.run_multi_process deadlock prevention."""

    def test_all_commands_succeed(self) -> None:
        """Verify normal operation when all commands succeed."""
        commands = [
            Command(identity="cmd1", command="echo hello", post_process=_noop_post_process),
            Command(identity="cmd2", command="echo world", post_process=_noop_post_process),
        ]
        runner = CommandRunner()
        results = runner.run_multi_process(commands)
        assert len(results) == len(commands)
        identities = {r.identity for r in results}
        assert identities == {"cmd1", "cmd2"}

    def test_crashing_post_process_does_not_deadlock(self) -> None:
        """Verify a crashing post_process is caught and does not cause a deadlock.

        Before the fix, this test would hang forever.
        """
        commands = [
            Command(identity="ok1", command="echo hello", post_process=_noop_post_process),
            Command(
                identity="crash",
                command="echo world",
                post_process=_crashing_post_process,
            ),
            Command(identity="ok2", command="echo foo", post_process=_noop_post_process),
        ]
        runner = CommandRunner()
        results = runner.run_multi_process(commands)
        assert len(results) == len(commands)
        crashed = next(r for r in results if r.identity == "crash")
        assert "Simulated crash" in crashed.errors

    def test_single_command_succeeds(self) -> None:
        """Verify run_multi_process works with a single command."""
        commands = [
            Command(identity="solo", command="echo solo", post_process=_noop_post_process),
        ]
        runner = CommandRunner()
        results = runner.run_multi_process(commands)
        assert len(results) == 1
        assert results[0].identity == "solo"

    def test_all_post_processes_crash(self) -> None:
        """Verify all commands complete even when every post_process crashes."""
        commands = [
            Command(identity="c1", command="echo a", post_process=_crashing_post_process),
            Command(identity="c2", command="echo b", post_process=_crashing_post_process),
        ]
        runner = CommandRunner()
        results = runner.run_multi_process(commands)
        assert len(results) == len(commands)
        for result in results:
            assert "Simulated crash" in result.errors


class TestStartWorkersReturnsProcesses:
    """Tests that start_workers returns process references."""

    def test_returns_process_list(self) -> None:
        """Verify start_workers returns a list of Process objects."""
        runner = CommandRunner()
        runner._completed_queue = multiprocessing.Manager().Queue()
        runner._pending_queue = multiprocessing.Manager().Queue()
        commands = [
            Command(identity="cmd1", command="echo hi", post_process=_noop_post_process),
        ]
        processes = runner.start_workers(commands)
        assert isinstance(processes, list)
        assert len(processes) >= 1
        for proc in processes:
            assert isinstance(proc, multiprocessing.Process)
        for proc in processes:
            proc.join(timeout=10)


class TestWorkerHealthCheck:
    """Tests for the timeout and worker health check paths in run_multi_process."""

    def test_raises_when_all_workers_dead(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify RuntimeError is raised when all workers die without completing.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        runner = CommandRunner()

        call_count = 0

        def _mock_get(timeout: int = 0) -> None:
            nonlocal call_count
            call_count += 1
            raise queue.Empty

        mock_queue = SimpleNamespace(get=_mock_get)
        runner._completed_queue = mock_queue  # type: ignore[assignment]
        runner._pending_queue = SimpleNamespace(put=lambda x: None)  # type: ignore[assignment]

        dead_worker = SimpleNamespace(is_alive=lambda: False, join=lambda: None)

        monkeypatch.setattr(runner, "start_workers", lambda jobs: [dead_worker])

        commands = [
            Command(identity="cmd1", command="echo hi", post_process=_noop_post_process),
        ]
        with pytest.raises(RuntimeError, match="All worker processes have terminated"):
            runner.run_multi_process(commands)

    def test_continues_when_workers_alive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Verify polling continues when workers are alive after a timeout.

        Args:
            monkeypatch: Pytest monkeypatch fixture
        """
        runner = CommandRunner()

        cmd = Command(identity="cmd1", command="echo hi", post_process=_noop_post_process)
        call_count = 0

        def _mock_get(timeout: int = 0) -> Command:
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise queue.Empty
            return cmd

        mock_queue = SimpleNamespace(get=_mock_get)
        runner._completed_queue = mock_queue  # type: ignore[assignment]
        runner._pending_queue = SimpleNamespace(put=lambda x: None)  # type: ignore[assignment]

        alive_worker = SimpleNamespace(is_alive=lambda: True, join=lambda: None)

        monkeypatch.setattr(runner, "start_workers", lambda jobs: [alive_worker])

        results = runner.run_multi_process([cmd])

        assert len(results) == 1
        assert results[0].identity == "cmd1"
