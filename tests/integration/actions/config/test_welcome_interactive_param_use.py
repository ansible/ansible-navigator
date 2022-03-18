"""Tests for ``config`` from welcome, interactive, with parameters.
"""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import BaseClass


CLI = Command(execution_environment=False).join()

steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(
        user_input=":config",
        comment="enter config from welcome screen",
        present=["Cache plugin timeout", "42"],
    ),
    UiTestStep(user_input=":back", comment="return to welcome screen"),
    UiTestStep(
        user_input=":config --ee True",
        comment="enter config from welcome screen",
        present=["Cache plugin timeout", "42"],
    ),
)

steps = add_indices(steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from welcome, interactive, with parameters."""

    UPDATE_FIXTURES = False
