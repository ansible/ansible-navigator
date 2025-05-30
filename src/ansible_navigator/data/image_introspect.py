"""Introspect an execution environment image."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading

from queue import Queue
from types import SimpleNamespace
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeAlias


if TYPE_CHECKING:
    from collections.abc import Callable

# https://github.com/python/typing/issues/182#issuecomment-1320974824
JSONTypes: TypeAlias = dict[str, "JSONTypes"] | list["JSONTypes"] | str | int | float | bool | None


class Command(SimpleNamespace):
    """Abstraction for a details about a shell command."""

    id_: str
    command: str
    parse: Callable[..., Any]
    stdout: str = ""
    stderr: str = ""
    details: list[str] | dict[Any, Any] | list[dict[Any, Any]] | str = ""
    errors: list[str] = []


def run_command(command: Command) -> None:
    """Run a command using subprocess.

    Args:
        command: Details of the command to run
    """
    try:
        proc_out = subprocess.run(
            command.command,
            capture_output=True,
            check=True,
            text=True,
            shell=True,
        )
        command.stdout = proc_out.stdout
    except subprocess.CalledProcessError as exc:
        command.stderr = str(exc.stderr)
        command.errors = [str(exc.stderr)]


def worker(pending_queue: Queue[Any], completed_queue: Queue[Any]) -> None:
    """Run a command from pending, parse, and place in completed.

    Args:
        pending_queue: A queue with plugins to process
        completed_queue: The queue in which extracted documentation will
            be placed
    """
    while True:
        command = pending_queue.get()
        if command is None:
            break
        run_command(command)
        try:
            command.parse(command)
        except Exception as exc:  # noqa: BLE001
            command.errors = command.errors + [str(exc)]
        completed_queue.put(command)


class CommandRunner:
    """A command runner.

    Run commands using single or multiple processes.
    """

    def __init__(self) -> None:
        """Initialize the command runner."""
        self._completed_queue: Queue[Any] | None = None
        self._pending_queue: Queue[Any] | None = None

    def run_multi_thread(self, command_classes: list[CmdParser]) -> list[CmdParser]:
        """Run commands with multiple threads.

        Workers are started to read from pending queue.
        Exit when the number of results is equal to the number
        of commands needing to be run.

        Args:
            command_classes: All command classes to be run

        Returns:
            The results from running all commands
        """
        if self._completed_queue is None:
            self._completed_queue = Queue()
        if self._pending_queue is None:
            self._pending_queue = Queue()
        all_commands = tuple(
            command for command_class in command_classes for command in command_class.commands
        )
        self.start_workers(all_commands)
        results: list[CmdParser] = []
        while len(results) != len(all_commands):
            results.append(self._completed_queue.get())
        return results

    def start_workers(self, jobs: tuple[Command, ...]) -> None:
        """Start workers and submit jobs to pending queue.

        Args:
            jobs: The jobs to be run

        Raises:
            RuntimeError: if there is a runtime error
        """
        worker_count = len(jobs)
        processes = []
        for _proc in range(worker_count):
            proc = threading.Thread(
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
        for proc in processes:
            proc.join()


class CmdParser:
    """A base class for command parsers with common parsing functions."""

    @property
    def commands(self) -> list[Command]:
        """List of commands to be executed."""
        return []

    @staticmethod
    def _strip(value: str) -> str:
        """Remove quotes, leading and trailing whitespace.

        Args:
            value: The string to act on

        Returns:
            The string after removing quotes, leading and trailing
            whitespace
        """
        return value.strip('"').strip("'").strip()

    @staticmethod
    def re_partition(content: Any, separator: str) -> Any:
        """Partition a string using a regular expression.

        Args:
            content: The content to partition
            separator: The separator to use for the partitioning

        Returns:
            The first partition, separator, and final partition
        """
        separator_match = re.search(separator, content)
        if not separator_match or content.startswith(" "):
            return "", "", content
        delim = separator_match.group(0)
        key, content = re.split(delim, content, maxsplit=1)
        return key, delim, content

    def splitter(
        self,
        lines: list[str],
        line_split: str,
        section_delim: str | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """Split lines given a delimiter.

        Args:
            lines: The lines to split
            line_split: The delimiter use for splitting each line
            section_delim: The separator between different packages

        Returns:
            All lines split on the delimiter
        """
        results: list[dict[str, Any]] = []
        result: dict[str, Any] = {}
        current_key: str = ""
        while lines:
            line = lines.pop(0)
            key, delim, content = self.re_partition(line, line_split)
            content = self._strip(content)
            if section_delim and line == section_delim:
                results.append(result)
                result = {}
                continue
            if not delim and current_key:
                result[current_key] += f" {content}"
                continue
            current_key = key.lower().replace("_", "-").strip()
            # system_packages description field needs special handling
            if current_key == "description":
                description = []
                while lines:
                    line = lines.pop(0)
                    if line == section_delim:
                        break
                    description.append(line)
                if description:
                    result[current_key] = " ".join(description)
                else:
                    result[current_key] = "No description available"
                results.append(result)
                return result
            result[current_key] = content

        if result:
            results.append(result)
        return results


class AnsibleCollections(CmdParser):
    """Available ansible collections collector."""

    @property
    def commands(self) -> list[Command]:
        """Define the ansible-galaxy command to list ansible collections.

        Returns:
            The defined command
        """
        command = "ansible-galaxy collection list"
        return [
            Command(
                id_="ansible_collections",
                command=command,
                parse=self.parse,
            ),
        ]

    @staticmethod
    def parse(command: Command) -> None:
        """Parse the output of the ansible-galaxy command.

        Args:
            command: The result of running the command
        """
        if "invalid choice: 'list'" in command.stderr:
            command.details = "This command is not supported with ansible 2.9."
            return
        collections = {}
        for line in command.stdout.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1][0].isdigit():
                collections[parts[0].strip()] = parts[1].strip()
        command.details = collections


class AnsibleVersion(CmdParser):
    """Ansible version collector."""

    @property
    def commands(self) -> list[Command]:
        """Define the ansible command to get the version.

        Returns:
            The defined command
        """
        return [Command(id_="ansible_version", command="ansible --version", parse=self.parse)]

    @staticmethod
    def parse(command: Command) -> None:
        """Parse the output of the ansible command.

        Args:
            command: The result of running the command
        """
        version = command.stdout.splitlines()[0]
        command.details = version


class OsRelease(CmdParser):
    """OS release information collector."""

    @property
    def commands(self) -> list[Command]:
        """Define the command to collect os release information.

        Returns:
            The defined command
        """
        return [Command(id_="os_release", command="cat /etc/os-release", parse=self.parse)]

    def parse(self, command: Command) -> None:
        """Parse the output of the cat command.

        Args:
            command: The result of running the command
        """
        parsed = self.splitter(command.stdout.splitlines(), "=")
        command.details = parsed


class PythonPackages(CmdParser):
    """Python package collector."""

    @property
    def commands(self) -> list[Command]:
        """Define the pip command to list installed pip packages.

        Returns:
            The defined command
        """
        pre = Command(
            id_="pip_freeze",
            command="/usr/bin/python3 -m pip freeze",
            parse=self.parse_freeze,
        )
        run_command(pre)
        pre.parse(pre)
        pkgs = " ".join(pkg for pkg in pre.details[0]) if pre.details else ""
        return [
            Command(
                id_="python_packages",
                command=f"/usr/bin/python3 -m pip show {pkgs}",
                parse=self.parse,
            ),
        ]

    def parse(self, command: Command) -> None:
        """Parse the output of the pip command.

        Args:
            command: The result of running the command
        """
        parsed = self.splitter(command.stdout.splitlines(), line_split=":", section_delim="---")
        if isinstance(parsed, dict):
            parsed = [parsed]
        for pkg in parsed:
            for entry in ["required-by", "requires"]:
                if pkg[entry]:
                    pkg[entry] = [p.strip() for p in pkg[entry].split(",")]
                else:
                    pkg[entry] = []
        command.details = parsed

    def parse_freeze(self, command: Command) -> None:
        """Parse the output of the pip freeze command, skipping editables.

        Args:
            command: The result of running the command
        """
        lines = [line for line in command.stdout.splitlines() if not line.startswith("-e")]
        parsed = self.splitter(lines, "(==|@)")
        command.details = parsed


class RedhatRelease(CmdParser):
    """Red Hat release collector."""

    @property
    def commands(self) -> list[Command]:
        """Define the command to get the redhat release information.

        Returns:
            The defined command
        """
        return [Command(id_="redhat_release", command="cat /etc/redhat-release", parse=self.parse)]

    @staticmethod
    def parse(command: Command) -> None:
        """Parse the output of the cat redhat release command.

        Args:
            command: The result of running the command
        """
        parsed = command.stdout
        command.details = parsed


class SystemPackages(CmdParser):
    """System packages collector."""

    @property
    def commands(self) -> list[Command]:
        """Define the command to list system packages.

        Returns:
            The defined command
        """
        return [Command(id_="system_packages", command="rpm -qai", parse=self.parse)]

    def parse(self, command: Command) -> None:
        """Parse the output of the rpm command.

        Args:
            command: The result of running the command
        """
        packages = []
        package: list[str] = []
        for line in command.stdout.splitlines():
            if re.match(r"^Name\s{2,}:", line) and package:
                packages.append(package)
                package = [line]
            else:
                package.append(line)
        if package:
            packages.append(package)

        parsed: list[Any] = []
        for package in packages:
            result = self.splitter(package, line_split=":")
            parsed.append(result)

        command.details = parsed


def main(serialize: bool = True) -> dict[str, JSONTypes] | None:
    """Enter the image introspection process.

    Args:
        serialize: Whether to serialize the results

    Returns:
        The collected data or none if serialize is False
    """
    response: dict[str, Any] = {"errors": []}
    response["python_version"] = {"details": {"version": " ".join(sys.version.splitlines())}}
    response["environment_variables"] = {"details": dict(os.environ)}
    try:
        command_runner = CommandRunner()
        commands: list[CmdParser] = [
            AnsibleCollections(),
            AnsibleVersion(),
            OsRelease(),
            RedhatRelease(),
            PythonPackages(),
            SystemPackages(),
        ]
        results = command_runner.run_multi_thread(commands)
        for result in results:
            result_as_dict = vars(result)
            result_as_dict.pop("parse")
            for key in list(result_as_dict.keys()):
                if key not in ["details", "errors"]:
                    result_as_dict[f"__{key}"] = result_as_dict[key]
                    result_as_dict.pop(key)
            response[result_as_dict["__id_"]] = result_as_dict
    except Exception as exc:  # noqa: BLE001
        response["errors"].append(str(exc))
    if serialize:
        print(json.dumps(response))
        return None
    return response


if __name__ == "__main__":
    main()
