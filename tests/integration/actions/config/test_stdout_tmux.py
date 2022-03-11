"""Tests for ``config`` from CLI, stdout."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import CONFIG_FIXTURE
from .base import BaseClass


class StdoutCommand(Command):
    """stdout command"""

    subcommand = "config"
    preclear = True


class ShellCommand(UiTestStep):
    """a shell command"""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="config dump with ee",
        user_input=StdoutCommand(
            cmdline="dump --senv PAGER=cat",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config dump without ee",
        user_input=StdoutCommand(
            cmdline="dump",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config list with ee",
        user_input=StdoutCommand(
            cmdline="list --senv PAGER=cat",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config list without ee",
        user_input=StdoutCommand(
            cmdline="dump",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config helpconfig with ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["usage: ansible-config [-h]"],
    ),
    ShellCommand(
        comment="config helpconfig without ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["usage: ansible-config [-h]"],
    ),
    ShellCommand(
        comment="config helpconfig with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="interactive",
            execution_environment=True,
        ).join(),
        present=["usage: ansible-config [-h]"],
    ),
    ShellCommand(
        comment="config helpconfig with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="interactive",
            execution_environment=False,
        ).join(),
        present=["usage: ansible-config [-h]"],
    ),
    ShellCommand(
        comment="config specified configuration file with ee",
        # pass the PAGER into the EE so the full contents return
        user_input=StdoutCommand(
            cmdline=f"dump -c {CONFIG_FIXTURE}",
            mode="stdout",
            execution_environment=True,
            pass_environment_variables=["PAGER"],
        ).join(),
        present=[".os2"],
    ),
    ShellCommand(
        comment="config specified configuration file without ee",
        user_input=StdoutCommand(
            cmdline=f"dump -c {CONFIG_FIXTURE}",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=[".os2"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
