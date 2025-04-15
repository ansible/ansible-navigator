"""Tests for ``config`` from CLI, stdout."""

import pytest

from tests.conftest import valid_ce as ce
from tests.integration._interactions import Command
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices

from .base import EE_MANIFEST
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
    ShellCommand(
        comment="build execution-environment without ee",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime {ce()} -v 3 -f {EE_MANIFEST}",
            mode="stdout",
            execution_environment=False,
        ).join(),
        present=["Hello from EE", "The build context can be found at"],
    ),
    ShellCommand(
        comment="build execution-environment with ee",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime {ce()} -v 3 -f {EE_MANIFEST}",
            mode="stdout",
            execution_environment=True,
        ).join(),
        present=["Hello from EE", "The build context can be found at"],
    ),
    ShellCommand(
        comment="build execution-environment without ee in interactive mode",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime {ce()} -v 3 -f {EE_MANIFEST}",
            mode="interactive",
            execution_environment=False,
        ).join(),
        present=["Hello from EE", "The build context can be found at"],
    ),
    ShellCommand(
        comment="build execution-environment with ee in interactive mode",
        user_input=StdoutCommand(
            cmdline=f"build --tag test_ee --container-runtime {ce()} -v 3 -f {EE_MANIFEST}",
            mode="interactive",
            execution_environment=True,
        ).join(),
        present=["Hello from EE", "The build context can be found at"],
    ),
)

steps = add_indices(stdout_tests)


@pytest.mark.skip(reason="builder tests are very slow and do not provide much value")
@pytest.mark.parametrize("step", steps)
class Test(BaseClass):
    """Run the tests for ``builder`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
