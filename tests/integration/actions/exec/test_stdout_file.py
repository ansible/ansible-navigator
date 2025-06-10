"""Tests for exec, mode stdout, parameters set using config file."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices

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
        present=["ANSIBLE_COLLECTIONS_PATH=/tmp/collections"],
    ),
)

steps = add_indices(stdout_tests)


def step_id(test_value: ShellCommand) -> str:
    """Return the test id from the test step object.

    Args:
        test_value: The data from the test iteration

    Returns:
        An id for the test
    """
    return f"{test_value.step_index}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for exec, mode stdout, parameters set using config file."""

    config_file = TEST_CONFIG_FILE
    update_fixtures = False
