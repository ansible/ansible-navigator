"""Tests for lint from CLI, interactive, with an EE."""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import LINT_FIXTURES
from .base import BaseClass


CLI = Command(subcommand="lint", cmdline=LINT_FIXTURES, execution_environment=True).join()

steps = (
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
    """Run the tests for lint from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
