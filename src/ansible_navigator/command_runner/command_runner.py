"""Definitions for the command runner."""
from __future__ import annotations

import multiprocessing
import subprocess

from dataclasses import dataclass
from dataclasses import field
from queue import Queue
from typing import Callable

from ansible_navigator.utils.definitions import LogMessage


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
    post_process: Callable
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""
    details: list = field(default_factory=list)
    errors: str = ""
    messages: list[LogMessage] = field(default_factory=list)

    @property
    def stderr_lines(self):
        """Produce a list of stderr lines.

        :returns: A list of stderr lines
        """
        return self.stderr.splitlines()

    @property
    def stdout_lines(self):
        """Produce a list of stdout lines.

        :returns: A list of stdout lines
        """
        return self.stdout.splitlines()


def run_command(command: Command) -> None:
    """Run a command.

    :param command: Command to be run
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


def worker(pending_queue: multiprocessing.Queue, completed_queue: multiprocessing.Queue) -> None:
    """Read pending, run, post process, and place in completed.

    :param pending_queue: All pending commands
    :param completed_queue: All completed commands
    """
    while True:
        command = pending_queue.get()
        if command is None:
            break
        run_command(command)
        command.post_process(command)
        completed_queue.put(command)


class CommandRunner:
    """Functionality for running commands."""

    def __init__(self):
        """Initialize the command runner."""
        self._completed_queue: Queue | None = None
        self._pending_queue: Queue | None = None

    @staticmethod
    def run_single_process(commands: list[Command]):
        """Run commands with a single process.

        :param commands: All commands to be run
        :returns: The results from running all commands
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

        :param commands: All commands to be run
        :returns: The results from running all commands
        """
        if self._completed_queue is None:
            self._completed_queue = multiprocessing.Manager().Queue()
        if self._pending_queue is None:
            self._pending_queue = multiprocessing.Manager().Queue()

        self.start_workers(commands)
        results: list[Command] = []
        while len(results) != len(commands):
            results.append(self._completed_queue.get())
        return results

    def start_workers(self, jobs):
        """Start the workers.

        :param jobs: List of commands to be run
        """
        worker_count = min(len(jobs), PROCESSES)
        processes = []
        for _proc in range(worker_count):
            proc = multiprocessing.Process(
                target=worker,
                args=(self._pending_queue, self._completed_queue),
            )
            processes.append(proc)
            proc.start()
        for job in jobs:
            self._pending_queue.put(job)
        for _proc in range(worker_count):
            self._pending_queue.put(None)
        for proc in processes:
            proc.join()
