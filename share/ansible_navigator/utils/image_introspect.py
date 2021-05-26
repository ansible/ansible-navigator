""" introspect an image """
import json
import re
import subprocess
import sys
import multiprocessing
from types import SimpleNamespace

from typing import Any
from typing import Callable, List
from typing import Dict
from typing import Union
from queue import Queue

# pylint: disable=broad-except

PROCESSES = (multiprocessing.cpu_count() - 1) or 1


class Command(SimpleNamespace):
    """command obj holder"""

    id: str
    command: str
    parse: Callable
    stdout: str = ""
    stderr: str = ""
    details: Union[List, Dict, str] = ""
    errors: List = []


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
        command.errors = [str(exc.stderr)]


def worker(pending_queue: multiprocessing.Queue, completed_queue: multiprocessing.Queue) -> None:
    """a worker, pulls from pending, runs & porcesses
    places in completed"""
    while True:
        command = pending_queue.get()
        if command is None:
            break
        run_command(command)
        try:
            command.parse(command)
        except Exception as exc:
            command.errors = command.errors + [str(exc)]
        completed_queue.put(command)


class CommandRunner:
    """runs commands"""

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
            try:
                command.parse(command)
            except Exception as exc:
                command.errors = command.errors + [str(exc)]
            results.append(command)
        return results

    def run_mproc(self, cmd_clss):
        """start the workers, unload the completed queue"""
        if self._completed_queue is None:
            self._completed_queue = multiprocessing.Manager().Queue()
        if self._pending_queue is None:
            self._pending_queue = multiprocessing.Manager().Queue()
        results = {}
        all_commands = tuple(cmd for cmd_cls in cmd_clss for cmd in cmd_cls.commands)
        self.start_workers(all_commands)
        results = []
        while len(results) != len(all_commands):
            results.append(self._completed_queue.get())
        return results

    def start_workers(self, jobs):
        """start workers, submit jobs to pending queue"""
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


class CmdParser:
    @staticmethod
    def re_partition(content, separator):
        """like partion, but uses an re"""
        separator_match = re.search(separator, content)
        if not separator_match:
            return content, "", ""
        matched_separator = separator_match.group(0)
        parts = re.split(matched_separator, content, 1)
        return parts[0], matched_separator, parts[1]

    def splitter(self, lines, delimiter):
        """split sections of delimited results"""
        results = []
        result = {}
        while lines:
            line = lines.pop()
            left, delim, right = self.re_partition(line, delimiter)
            right = right.strip('"').strip("'").strip()
            if not delim:
                if result:
                    results.append(result)
                    result = {}
                continue
            while not left.strip():
                line = lines.pop()
                left, delim, more_right = self.re_partition(line, delimiter)
                more_right = more_right.strip('"').strip("'").strip()
                right = more_right + " " + right
            key = left.lower().replace("_", "-").strip()
            value = right
            result[key] = value
        if result:
            results.append(result)
        return results


class AnsibleCollections(CmdParser):
    """collect ansible collections"""

    @property
    def commands(self):
        command = "ansible-galaxy collection list"
        return [
            Command(
                id="ansible_collections",
                command=command,
                parse=self.parse,
            )
        ]

    def parse(self, command: Command):
        """parse"""
        collections = {}
        for line in command.stdout.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1][0].isdigit():
                collections[parts[0].strip()] = parts[1].strip()
        command.details = collections


class AnsibleVersion(CmdParser):
    """collect ansible version"""

    @property
    def commands(self) -> List[Command]:
        """generate the command"""
        return [Command(id="ansible_version", command="ansible --version", parse=self.parse)]

    def parse(self, command: Command) -> None:
        """parse"""
        version = command.stdout.splitlines()[0].split(" ", 1)[1].strip()[1:-1]
        command.details = version


class OsRelease(CmdParser):
    """collect os release info"""

    @property
    def commands(self) -> List[Command]:
        """generate the command"""
        return [Command(id="os_release", command="cat /etc/os-release", parse=self.parse)]

    def parse(self, command) -> None:
        """parse"""
        parsed = self.splitter(command.stdout.splitlines(), "=")
        command.details = parsed


class PythonPackages(CmdParser):
    """collect python packages"""

    @property
    def commands(self) -> List[Command]:
        """generate the command"""
        pre = Command(id="pip_freeze", command="python3 -m pip freeze", parse=self.parse_freeze)
        run_command(pre)
        pre.parse(pre)
        pkgs = " ".join(pkg for pkg in pre.details[0])
        return [
            Command(id="python_packages", command=f"python3 -m pip show {pkgs}", parse=self.parse)
        ]

    def parse(self, command):
        """parse"""
        parsed = self.splitter(command.stdout.splitlines(), ":")
        for pkg in parsed:
            for entry in ["required-by", "requires"]:
                if pkg[entry]:
                    pkg[entry] = [p.strip() for p in pkg[entry].split(",")]
                else:
                    pkg[entry] = []
        command.details = parsed

    def parse_freeze(self, command):
        """parse pip freeze"""
        # skip the editiables
        lines = [line for line in command.stdout.splitlines() if not line.startswith("-e")]
        parsed = self.splitter(lines, "(==|@)")
        command.details = parsed


class RedhatRelease(CmdParser):
    """collect rh release"""

    @property
    def commands(self) -> List[Command]:
        """generate the command"""
        return [Command(id="redhat_release", command="cat /etc/redhat-release", parse=self.parse)]

    def parse(self, command):
        """parse"""
        parsed = command.stdout
        command.details = parsed


class SystemPackages(CmdParser):
    """collect system pkgs"""

    @property
    def commands(self) -> List[Command]:
        """generate the command"""
        return [Command(id="system_packages", command="yum info installed", parse=self.parse)]

    def parse(self, command):
        """parse"""
        parsed = self.splitter(command.stdout.splitlines(), ":")
        command.details = parsed


def main():
    """start here"""
    response = {"errors": []}
    response["python_version"] = {"details": {"version": " ".join(sys.version.splitlines())}}
    try:
        command_runner = CommandRunner()
        commands = [
            AnsibleCollections(),
            AnsibleVersion(),
            OsRelease(),
            RedhatRelease(),
            PythonPackages(),
            SystemPackages(),
        ]
        results = command_runner.run_mproc(commands)
        for result in results:
            dicted = vars(result)
            dicted.pop("parse")
            for key in list(dicted.keys()):
                if key not in ["details", "errors"]:
                    dicted[f"__{key}"] = dicted[key]
                    dicted.pop(key)
            response[dicted["__id"]] = dicted
    except Exception as exc:
        response["errors"].append(str(exc))
    print(json.dumps(response))


if __name__ == "__main__":
    main()
