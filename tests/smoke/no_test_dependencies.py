"""Tests ensuring only requirements.txt are needed."""

import os
import shutil
import tempfile
import unittest  # pylint: disable=preferred-module
import uuid

from dataclasses import dataclass
from pathlib import Path
from typing import List
from typing import Tuple

from ansible_navigator.command_runner import Command
from ansible_navigator.command_runner import CommandRunner


def _get_venv():
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path is None:
        raise AssertionError(
            "VIRTUAL_ENV environment variable was not set but tox should have set it.",
        )
    venv = Path(venv_path, "bin", "activate")
    return venv


@dataclass
class NavigatorCommand(Command):
    """Data structure for a full command."""

    ee_tests: Tuple[bool, bool] = (True, False)
    find: str = ""
    set_env: str = "--senv PAGER=cat"

    def __post_init__(self):
        """Post the init."""
        self.identity = self.command
        venv = _get_venv()
        self.command = f". {venv} && ansible-navigator {self.command} {self.set_env}"


@dataclass
class PartialCommand:
    """The unique parts of one command."""

    params: str
    find: str
    ee_support: Tuple[bool, ...] = (True, False)


PartialCommands = (
    PartialCommand(params="--help", find="Start at the welcome page"),
    PartialCommand(params="builder --help-builder", find="Print ansible-builder version"),
    PartialCommand(params="config list --mode stdout", find="Valid YAML extensions"),
    PartialCommand(params="doc debug --mode stdout", find="ansible.builtin.debug"),
    PartialCommand(params="exec whoami", find="root", ee_support=(True,)),
    PartialCommand(params="run --help-playbook", find="--become"),
)


def _generate_commands(tmp_dir: Path) -> List[NavigatorCommand]:
    """Produce the commands.

    :param tmp_dir: Path to a temporary directory
    :returns: All the commands
    """
    commands: List[NavigatorCommand] = []
    for partial_command in PartialCommands:
        for ee_value in partial_command.ee_support:
            random_name = uuid.uuid4()
            artifact_file = tmp_dir / f"{random_name}.json"
            log_file = tmp_dir / f"{random_name}.txt"
            append = f"--lf {log_file} --pas {artifact_file!s} --ee {ee_value!s}"
            nav_cmd = NavigatorCommand(
                find=partial_command.find,
                identity=partial_command.params,
                command=f"{partial_command.params} {append}",
                post_process=_post_process,
            )
            commands.append(nav_cmd)
    return commands


def _post_process(*_args, **_kwargs) -> None:
    """Do nothing command post processor.

    :param _args: The arguments
    :param _kwargs: The keyword arguments
    """


class Test(unittest.TestCase):
    """The smoke tests."""

    def setUp(self) -> None:
        """Create a temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        """Remove the directory after the test."""
        shutil.rmtree(self.test_dir)

    def test(self):
        """Execute the smoke tests."""
        tmp_dir = self.test_dir
        commands = _generate_commands(tmp_dir)
        command_results = CommandRunner().run_multi_proccess(commands)
        for command in command_results:
            with self.subTest():
                print(command.command)
                self.assertIn(
                    command.find,
                    command.stdout,
                    msg=(
                        f"command: {command.command},"
                        f" stdout: {command.stdout},"
                        f" stderr: {command.stderr}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
