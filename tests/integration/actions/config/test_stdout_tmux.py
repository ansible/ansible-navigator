"""Tests for config from cli, stdout."""
import pytest


from .base import BaseClass
from .base import CONFIG_FIXTURE

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._interactions import add_indicies


class StdoutCommand(Command):
    """stdout command"""

    subcommand = "config"
    preclear = True


class ShellCommand(Step):
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
        look_fors=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config dump without ee",
        user_input=StdoutCommand(
            cmdline="dump",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config list with ee",
        user_input=StdoutCommand(
            cmdline="list --senv PAGER=cat",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config list without ee",
        user_input=StdoutCommand(
            cmdline="dump",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["YAML_FILENAME_EXTENSIONS"],
    ),
    ShellCommand(
        comment="config helpconfig with ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="stdout",
            execution_environment=True,
        ).join(),
        look_fors=["usage: ansible-config [-h]"],
    ),
    ShellCommand(
        comment="config helpconfig without ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=["usage: ansible-config [-h]"],
    ),
    ShellCommand(
        comment="config helpconfig fail with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="interactive",
            execution_environment=True,
        ).join(),
        look_fors=["--hc or --help-config is valid only when 'mode' argument is set to 'stdout'"],
    ),
    ShellCommand(
        comment="config helpconfig fail with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-config",
            mode="interactive",
            execution_environment=False,
        ).join(),
        look_fors=["--hc or --help-config is valid only when 'mode' argument is set to 'stdout'"],
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
        look_fors=[".yahmool"],
    ),
    ShellCommand(
        comment="config specified configuration file without ee",
        user_input=StdoutCommand(
            cmdline=f"dump -c {CONFIG_FIXTURE}",
            mode="stdout",
            execution_environment=False,
        ).join(),
        look_fors=[".yahmool"],
    ),
)

steps = add_indicies(stdout_tests)


def step_id(value):
    """return the test id from the test step object"""
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for config from cli, mode stdout."""

    UPDATE_FIXTURES = False
