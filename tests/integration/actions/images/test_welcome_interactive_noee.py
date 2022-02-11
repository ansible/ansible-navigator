"""Tests for images from CLI, interactive, without an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import IMAGE_SHORT
from .base import BaseClass
from .base import base_steps


# this is misleading b/c images will use an EE, but not for automation
CLI = Command(execution_environment=False).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(
        user_input=":images",
        comment="ansible-navigator images top window",
        present=[IMAGE_SHORT],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for images from welcome, interactive, without an EE."""

    UPDATE_FIXTURES = False
