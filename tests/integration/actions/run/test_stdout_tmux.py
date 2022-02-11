"""Tests for run from CLI, stdout."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import BaseClass
from .base import inventory_path
from .base import playbook_path


class StdoutCommand(Command):
    """stdout command"""

    subcommand = "run"
    preclear = True


class ShellCommand(UiTestStep):
    """a shell command"""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="run playbook with ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["TASK [debug print play-3 task-2]", "ok=6", "failed=0"],
    ),
    ShellCommand(
        comment="run playbook without ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["TASK [debug print play-3 task-2]", "ok=6", "failed=0"],
    ),
    ShellCommand(
        comment="playbook help with ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["usage: ansible-playbook [-h]"],
    ),
    ShellCommand(
        comment="playbook help without ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["usage: ansible-playbook [-h]"],
    ),
    ShellCommand(
        comment="run help-playbook fail with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="interactive",
            execution_environment=True,
        ).join(),
        present=["--hp or --help-playbook is valid only when 'mode' argument is set to 'stdout'"],
    ),
    ShellCommand(
        comment="run help-playbook fail with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-playbook",
            mode="interactive",
            execution_environment=False,
        ).join(),
        present=["--hp or --help-playbook is valid only when 'mode' argument is set to 'stdout'"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for run from CLI, stdout."""

    UPDATE_FIXTURES = False
