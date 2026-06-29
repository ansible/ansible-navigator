"""Definitions for the command runner."""

from __future__ import annotations

import logging
import multiprocessing
import queue
import subprocess

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any


if TYPE_CHECKING:
    from collections.abc import Callable
    from queue import Queue

    from ansible_navigator.utils.definitions import LogMessage

logger = logging.getLogger(__name__)

_WORKER_TIMEOUT = 30


PROCESSES = (multiprocessing.cpu_count() - 1) or 1


@dataclass(frozen=False)
class Command:
    """Data structure for details of a command to be run.

    A ``Command`` is updated after instantiated with details from either
    ``stdout`` or ``stderr``.
    """

    # pylint: disable=too-many-instance-attributes
    identity: str
    command: str
    post_process: Callable[..., Any]
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""
    details: list[Any] | dict[Any, Any] | object = field(default_factory=list)
    errors: str = ""
    messages: list[LogMessage] = field(default_factory=list)

    @property
    def stderr_lines(self) -> list[str]:
        """Produce a list of stderr lines.

        Returns:
            A list of stderr lines
        """
        return self.stderr.splitlines()

    @property
    def stdout_lines(self) -> list[str]:
        """Produce a list of stdout lines.

        Returns:
            A list of stdout lines
        """
        return self.stdout.splitlines()


def run_command(command: Command) -> None:
    """Run a command.

    Args:
        command: Command to be run
    """
    try:
        proc_out = subprocess.run(
            command.command,
            capture_output=True,
            check=True,
            text=True,
            shell=True,
        )
        command.return_code = proc_out.returncode
        command.stdout = proc_out.stdout
    except subprocess.CalledProcessError as exc:
        command.return_code = exc.returncode
        command.stdout = str(exc.stdout)
        command.stderr = str(exc.stderr)


def worker(
    pending_queue: multiprocessing.Queue[Any],
    completed_queue: multiprocessing.Queue[Any],
) -> None:
    """Read pending, run, post process, and place in completed.

    Args:
        pending_queue: All pending commands
        completed_queue: All completed commands
    """
    while True:
        command = pending_queue.get()
        if command is None:
            break
        run_command(command)
        try:
            command.post_process(command)
        except Exception as exc:
            command.errors = str(exc)
            logger.exception("post_process failed for command %s", command.identity)
        completed_queue.put(command)


class CommandRunner:
    """Functionality for running commands."""

    def __init__(self) -> None:
        """Initialize the command runner."""
        self._completed_queue: Queue[Any] | None = None
        self._pending_queue: Queue[Command | None] | None = None

    @staticmethod
    def run_single_process(commands: list[Command]) -> list[Command]:
        """Run commands with a single process.

        Args:
            commands: All commands to be run

        Returns:
            The results from running all commands
        """
        results: list[Command] = []
        for command in commands:
            run_command(command)
            command.post_process(command)
            results.append(command)
        return results

    def run_multi_process(self, commands: list[Command]) -> list[Command]:
        """Run commands with multiple processes.

        Workers are started to read from pending queue.
        Exit when the number of results is equal to the number
        of commands needing to be run.

        Args:
            commands: All commands to be run

        Returns:
            The results from running all commands

        Raises:
            RuntimeError: If all workers terminate before all commands complete
        """
        if self._completed_queue is None:
            self._completed_queue = multiprocessing.Manager().Queue()
        if self._pending_queue is None:
            self._pending_queue = multiprocessing.Manager().Queue()

        workers = self.start_workers(commands)
        results: list[Command] = []
        while len(results) != len(commands):
            try:
                result = self._completed_queue.get(timeout=_WORKER_TIMEOUT)
                results.append(result)
            except queue.Empty:
                alive_workers = [w for w in workers if w.is_alive()]
                if not alive_workers:
                    failed = len(commands) - len(results)
                    msg = (
                        f"All worker processes have terminated but {failed} of "
                        f"{len(commands)} commands did not complete. "
                        f"Worker processes may have crashed."
                    )
                    raise RuntimeError(msg)  # noqa: B904
                logger.debug(
                    "Waiting for %d workers (%d/%d results collected)",
                    len(alive_workers),
                    len(results),
                    len(commands),
                )
        for w in workers:
            w.join()
        return results

    def start_workers(self, jobs: list[Command]) -> list[multiprocessing.Process]:
        """Start the workers.

        Args:
            jobs: List of commands to be run

        Returns:
            The list of started worker processes

        Raises:
            RuntimeError: if the pending queue is not initialized
        """
        worker_count = min(len(jobs), PROCESSES)
        processes: list[multiprocessing.Process] = []
        for _proc in range(worker_count):
            proc = multiprocessing.Process(
                target=worker,
                args=(self._pending_queue, self._completed_queue),
            )
            processes.append(proc)
            proc.start()
        if not self._pending_queue:
            raise RuntimeError
        for job in jobs:
            self._pending_queue.put(job)
        for _proc in range(worker_count):
            self._pending_queue.put(None)
        return processes
