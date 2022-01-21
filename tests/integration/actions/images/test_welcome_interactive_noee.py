"""Tests for images from CLI, interactive, without an EE.
"""
import pytest

from .base import IMAGE_SHORT
from .base import BaseClass
from .base import base_steps
from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id


# this is misleading b/c images will use an EE, but not for automation
CLI = Command(execution_environment=False).join()

initial_steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(
        user_input=":images",
        comment="ansible-navigator images top window",
        look_fors=[IMAGE_SHORT],
    ),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for images from welcome, interactive, without an EE."""

    UPDATE_FIXTURES = False
