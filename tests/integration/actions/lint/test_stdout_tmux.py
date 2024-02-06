"""Tests for ``lint`` from CLI, stdout."""

import os

import pytest

from tests.defaults import id_func
from tests.integration._interactions import Command
from tests.integration._interactions import SearchFor
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices

from .base import LINT_FIXTURES
from .base import BaseClass


stdout_tests = (
    UiTestStep(
        comment="lint stdout with errors",
        user_input=Command(
            subcommand="lint",
            cmdline=LINT_FIXTURES,
            precommand=f"cd {os.path.join(LINT_FIXTURES, '..')} ; ",
            mode="stdout",
            execution_environment=True,
            preclear=True,
        ).join(),
        present=["Commands should not change things"],
        search_within_response=SearchFor.PROMPT,
    ),
    UiTestStep(
        comment="lint stdout with no errors",
        user_input=Command(
            subcommand="lint",
            cmdline=os.path.join(LINT_FIXTURES, "no_errors"),
            mode="stdout",
            execution_environment=True,
        ).join(),
        absent=[".yml:"],
        search_within_response=SearchFor.PROMPT,
    ),
)

steps = add_indices(stdout_tests)


@pytest.mark.parametrize("step", steps, ids=id_func)
class Test(BaseClass):
    """Run the tests for ``lint`` from CLI, mode stdout."""

    UPDATE_FIXTURES = False
