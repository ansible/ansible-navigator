""" command runner """
import multiprocessing
from queue import Queue
import subprocess

from typing import Any
from typing import Callable
from typing import List
from typing import Union

from types import SimpleNamespace

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
        self._completed_queue: Union[Queue, None] = None
        self._pending_queue: Union[Queue, None] = None

    @staticmethod
    def run_sproc(cmd_clss: Any):
        """run with a sinlge proc"""
        all_commands = tuple(cmd for cmd_cls in cmd_clss for cmd in cmd_cls.commands)
        results = []
        for command in all_commands:
            run_command(command)
            command.post_process(command)
            results.append(command)
        return results

    def run_mproc(self, cmd_clss: Any):
        """run multiple proc"""
        if self._completed_queue is None:
            self._completed_queue = multiprocessing.Manager().Queue()
        if self._pending_queue is None:
            self._pending_queue = multiprocessing.Manager().Queue()
        all_commands = tuple(cmd for cmd_cls in cmd_clss for cmd in cmd_cls.commands)
        self.start_workers(all_commands)
        results: List[Command] = []
        while len(results) != len(all_commands):
            results.append(self._completed_queue.get())
        return results

    def start_workers(self, jobs):
        """start the workers"""
        worker_count = min(len(jobs), PROCESSES)
        processes = []
        for _proc in range(worker_count):
            proc = multiprocessing.Process(
                target=worker, args=(self._pending_queue, self._completed_queue)
            )
            processes.append(proc)
            proc.start()
        for job in jobs:
            self._pending_queue.put(job)
        for _proc in range(worker_count):
            self._pending_queue.put(None)
        for proc in processes:
            proc.join()
