"""Tests for ``config`` from CLI, interactive, without an EE.
"""
import pytest

from .base import base_steps
from .base import BaseClass

from ..._interactions import add_indicies
from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import step_id

CLI = Command(execution_environment=False).join()

initial_steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(
        user_input=":config",
        comment="enter config from welcome screen",
        look_fors=["ACTION_WARNINGS", "CALLBACKS_ENABLED"],
    ),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
