"""Tests for ``collections`` from CLI, stdout."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import BaseClass


class StdoutCommand(Command):
    """A stdout command."""

    subcommand = "collections"


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="collections with ee",
        user_input=StdoutCommand(
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["- collection_info:", "  name: ansible.builtin", "  roles:"],
    ),
    ShellCommand(
        comment="collections without ee",
        user_input=StdoutCommand(
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["- collection_info:", "    namespace: company_name", "  roles:"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(value):
    """Return the test id from the test step object.

    :param value: The value from which the test id will be generated
    :returns: The id for the test
    """
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``collections`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
