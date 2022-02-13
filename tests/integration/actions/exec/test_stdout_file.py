"""Tests for exec, mode stdout, parameters set using config file."""

import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from .base import TEST_CONFIG_FILE
from .base import BaseClass


class StdoutCommand(Command):
    """A stdout command."""

    mode = "stdout"
    subcommand = "exec"
    preclear = True


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="exec echo with ee",
        user_input=StdoutCommand(
            execution_environment=True,
        ).join(),
        present=["bash", "test_data_from_config"],
        absent=["ERROR"],
    ),
    ShellCommand(
        comment="exec echo check no path via shell",
        user_input=StdoutCommand(
            cmdline="'/usr/bin/echo $PATH'",
            execution_environment=True,
        ).join(),
        absent=["/sbin"],
    ),
    ShellCommand(
        comment="ensure env vars get set from config",
        user_input=StdoutCommand(
            cmdline="/bin/env",
            execution_environment=True,
        ).join(),
        present=["ANSIBLE_COLLECTIONS_PATHS=/tmp/collections"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(test_value: ShellCommand) -> str:
    """Return the test id from the test step object.

    :param test_value: The data from the test iteration
    :returns: An id for the test
    """
    return f"{test_value.comment}  {test_value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for exec, mode stdout, parameters set using config file."""

    config_file = TEST_CONFIG_FILE
    update_fixtures = False
