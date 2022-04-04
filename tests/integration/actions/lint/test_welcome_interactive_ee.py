"""Tests for lint from welcome, interactive, with an EE."""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import LINT_FIXTURES
from .base import BaseClass


CLI = Command(execution_environment=True).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(
        user_input=f":lint {LINT_FIXTURES}",
        comment="ansible-navigator lint results list",
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

steps = add_indices(initial_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for lint from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
