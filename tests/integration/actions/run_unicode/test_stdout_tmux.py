"""Tests for run from CLI, stdout, with unicode."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import BaseClass
from .base import inventory_path
from .base import playbook_path


class StdoutCommand(Command):
    """A command to run in the terminal."""

    subcommand = "run"
    preclear = True


class ShellCommand(UiTestStep):
    """A test step, specifically in mode stdout."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="run playbook with ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["航海家", "ok=2", "failed=0"],
    ),
    ShellCommand(
        comment="run playbook without ee",
        user_input=StdoutCommand(
            cmdline=f"{playbook_path} -i {inventory_path} --pae false",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["航海家", "ok=2", "failed=0"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(value):
    """Return a test id for the test step object.

    :param value: The data to generate the id from
    :returns: The test id
    """
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for run from CLI, stdout."""

    UPDATE_FIXTURES = False
