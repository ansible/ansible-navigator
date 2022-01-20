"""Tests for images from welcome, interactive, with an EE.
"""
import pytest

from .base import IMAGE_SHORT
from .base import BaseClass
from .base import base_steps
from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id

CLI = Command(execution_environment=True).join()

initial_steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(
        user_input=":images", comment="ansible-navigator images top window", look_fors=[IMAGE_SHORT]
    ),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for images from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
