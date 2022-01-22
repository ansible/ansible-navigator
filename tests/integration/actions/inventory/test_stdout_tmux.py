"""Tests for inventory from CLI, stdout."""
import pytest

from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._interactions import add_indicies


class StdoutCommand(Command):
    """stdout command"""

    subcommand = "inventory"
    preclear = True


class ShellCommand(Step):
    """a shell command"""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="inventory list with ee",
        user_input=StdoutCommand(
            cmdline=f"--list -i {ANSIBLE_INVENTORY_FIXTURE_DIR}",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["_meta", "group03"],
    ),
    ShellCommand(
        comment="inventory list without ee",
        user_input=StdoutCommand(
            cmdline=f"--list -i {ANSIBLE_INVENTORY_FIXTURE_DIR}",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["_meta", "group03"],
    ),
    ShellCommand(
        comment="inventory help with ee",
        user_input=StdoutCommand(
            cmdline="--help-inventory",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["usage: ansible-inventory [-h]"],
    ),
    ShellCommand(
        comment="inventory help without ee",
        user_input=StdoutCommand(
            cmdline="--help-inventory",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["usage: ansible-inventory [-h]"],
    ),
    ShellCommand(
        comment="inventory help-inventory fail with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-inventory",
            mode="interactive",
            execution_environment=True,
        ).join(),
        look_fors=[
            "--hi or --help-inventory is valid only when 'mode' argument is set to 'stdout'",
        ],
    ),
    ShellCommand(
        comment="inventory help-inventory fail with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-inventory",
            mode="interactive",
            execution_environment=False,
        ).join(),
        look_fors=[
            "--hi or --help-inventory is valid only when 'mode' argument is set to 'stdout'",
        ],
    ),
)

steps = add_indicies(stdout_tests)


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, stdout."""

    UPDATE_FIXTURES = False
