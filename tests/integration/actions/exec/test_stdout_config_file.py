"""Tests for exec, mode stdout, parameters set using config file."""

import pytest


from .base import BaseClass
from .base import TEST_CONFIG_FILE

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import Step
from ..._interactions import add_indicies


class StdoutCommand(Command):
    """A stdout command."""

    mode = "stdout"
    subcommand = "exec"
    preclear = True


class ShellCommand(Step):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="exec echo with ee",
        user_input=StdoutCommand(
            execution_environment=True,
        ).join(),
        look_fors=["bash", "test_data_from_config"],
        look_nots=["ERROR"],
    ),
    ShellCommand(
        comment="exec echo check no path via shell",
        user_input=StdoutCommand(
            cmdline="--excmd '/usr/bin/echo $PATH'",
            execution_environment=True,
        ).join(),
        look_nots=["/sbin"],
    ),
)

steps = add_indicies(stdout_tests)


def step_id(value: ShellCommand) -> str:
    """Return the test id from the test step object.

    :param value: The data fro the test iteration
    :returns: An id for the test
    """
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for exec, mode stdout, parameters set using config file."""

    CONFIG_FILE = TEST_CONFIG_FILE
    UPDATE_FIXTURES = False
