"""Tests for ``config`` from CLI, interactive, without an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import BaseClass
from .base import base_steps


CLI = Command(subcommand="config", execution_environment=False).join()

initial_steps = (
    Step(
        user_input=CLI,
        comment="ansible-navigator config command top window",
        look_fors=["ACTION_WARNINGS", "CALLBACKS_ENABLED"],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
