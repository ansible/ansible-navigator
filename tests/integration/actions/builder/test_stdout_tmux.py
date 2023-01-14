"""Tests for ``config`` from CLI, stdout."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices

# from .base import BUILDER_FIXTURE
from .base import BaseClass


class StdoutCommand(Command):
    """A stdout command."""

    subcommand = "builder"
    preclear = True


class ShellCommand(UiTestStep):
    """A shell command."""

    search_within_response = SearchFor.PROMPT


stdout_tests = (
    ShellCommand(
        comment="builder help-builder with ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["usage: ansible-builder [-h]"],
    ),
    ShellCommand(
        comment="builder help-builder without ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["usage: ansible-builder [-h]"],
    ),
    ShellCommand(
        comment="builder help-builder with interactive with ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="interactive",
            execution_environment=True,
        ).join(),
        present=["usage: ansible-builder [-h]"],
    ),
    ShellCommand(
        comment="builder help-builder with interactive without ee",
        user_input=StdoutCommand(
            cmdline="--help-builder",
            mode="interactive",
            execution_environment=False,
        ).join(),
        present=["usage: ansible-builder [-h]"],
    ),
    # In the interest of time, we are not testing the following
    # until we can find a faster, more reliable way to run these
    # they are disabled.
    # Once caching with GHA is in place we should uncomment one and see
    # the time it takes to run is the container has previously been built and cached
    #
    # ShellCommand(
    #     comment="build execution-environment without ee",
    #     user_input=StdoutCommand(
    #         cmdline=f"build --tag test_ee --container-runtime \
    #                  docker -v 3  --workdir {BUILDER_FIXTURE}",
    #         mode="stdout",
    #         execution_environment=False,
    #     ).join(),
    #     present=["Hello from EE", "The build context can be found at"],
    # ),
    # ShellCommand(
    #     comment="build execution-environment with ee",
    #     user_input=StdoutCommand(
    #         cmdline=f"build --tag test_ee --container-runtime docker -v 3 \
    #                  --workdir {BUILDER_FIXTURE}",
    #         mode="stdout",
    #         execution_environment=True,
    #     ).join(),
    #     present=["Hello from EE", "The build context can be found at"],
    # ),
    # ShellCommand(
    #     comment="build execution-environment without ee in interactive mode",
    #     user_input=StdoutCommand(
    #         cmdline=f"build --tag test_ee --container-runtime docker -v 3 \
    #                   --workdir {BUILDER_FIXTURE}",
    #         mode="interactive",
    #         execution_environment=False,
    #     ).join(),
    #     present=["Hello from EE", "The build context can be found at"],
    # ),
    # ShellCommand(
    #     comment="build execution-environment with ee in interactive mode",
    #     user_input=StdoutCommand(
    #         cmdline=f"build --tag test_ee --container-runtime docker -v 3 \
    #                   --workdir {BUILDER_FIXTURE}",
    #         mode="interactive",
    #         execution_environment=True,
    #     ).join(),
    #     present=["Hello from EE", "The build context can be found at"],
    # ),
)

steps = add_indices(stdout_tests)


def step_id(value):
    """Return the test id from the test step object.

    :param value: The parameterized value from which the id will be generated
    :returns: A formatted id for the test
    """
    return f"{value.comment}  {value.user_input}"


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``builder`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
