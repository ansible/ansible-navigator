"""command runner"""
import multiprocessing
import subprocess

from queue import Queue
from types import SimpleNamespace
from typing import Callable
from typing import List
from typing import Union


PROCESSES = (multiprocessing.cpu_count() - 1) or 1


class Command(SimpleNamespace):
    # pylint: disable=too-few-public-methods
    """command obj"""

    id: str
    command: str
    post_process: Callable
    stdout: str = ""
    stderr: str = ""
    details: List = []
    errors: str = ""


def run_command(command: Command) -> None:
    """run a command"""
    try:
        proc_out = subprocess.run(
            command.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
            shell=True,
        )
        command.stdout = proc_out.stdout
    except subprocess.CalledProcessError as exc:
        command.stderr = str(exc.stderr)


def worker(pending_queue: multiprocessing.Queue, completed_queue: multiprocessing.Queue) -> None:
    """read pending, run, post process, place in completed"""
    while True:
        command = pending_queue.get()
        if command is None:
            break
        run_command(command)
        command.post_process(command)
        completed_queue.put(command)


class CommandRunner:
    """I run commands"""

    def __init__(self):
        """Initialize the command runner."""
        self._completed_queue: Union[Queue, None] = None
        self._pending_queue: Union[Queue, None] = None

    @staticmethod
    def run_single_proccess(commands: List[Command]):
        """Run commands with a single process.

        :param commands: All commands to be run
        :returns: The results from running all commands
        """
        results: List[Command] = []
        for command in commands:
            run_command(command)
            command.post_process(command)
            results.append(command)
        return results

    def run_multi_proccess(self, commands: List[Command]) -> List[Command]:
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
        results: List[Command] = []
        while len(results) != len(commands):
            results.append(self._completed_queue.get())
        return results

    def start_workers(self, jobs):
        """start the workers"""
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
