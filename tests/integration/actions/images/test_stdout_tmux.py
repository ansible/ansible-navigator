"""Tests for ``images`` from CLI, stdout."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import BaseClass


class StdoutCommand(Command):
    """Stdout command."""

    subcommand = "images"
    preclear = True


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="print image to stdout",
        user_input=StdoutCommand(
            cmdline="",
            mode="stdout",
            execution_environment=True,
            raw_append=" | grep creator",
        ).join(),
        present=["repository: quay.io/ansible/creator-ee"],
    ),
)

steps = add_indices(stdout_tests)


@pytest.mark.parametrize("step", steps, ids=str)
class Test(BaseClass):
    """Run the tests for ``images`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
