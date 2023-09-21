"""Tests for lint from CLI, interactive, without an EE."""
import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id

from .base import LINT_FIXTURES
from .base import BaseClass


CLI = Command(subcommand="lint", cmdline=LINT_FIXTURES, execution_environment=False).join()

steps: tuple[UiTestStep, ...] = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator lint top window",
        present=["All tasks should be named"],
    ),
    UiTestStep(
        user_input=":2",
        comment="lint result content page",
        present=["issue_path:"],
    ),
    UiTestStep(
        user_input=":back",
        comment="ansible-navigator lint top window",
        present=["All tasks should be named"],
    ),
)

steps = add_indices(steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for lint from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
