"""Tests for lint from welcome, interactive, without an EE."""
import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id

from .base import LINT_FIXTURES
from .base import BaseClass


CLI = Command(execution_environment=False).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(
        user_input=f":lint {LINT_FIXTURES}",
        comment="ansible-navigator lint result without EE",
        present=["Issues were found while applying the settings"],
    ),
)

steps = add_indices(initial_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for lint from welcome, interactive, without an EE."""

    UPDATE_FIXTURES = False
