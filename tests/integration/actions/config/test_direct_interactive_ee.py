"""Tests for ``config`` from CLI, interactive, with an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import BaseClass
from .base import base_steps


CLI = Command(subcommand="config", execution_environment=True).join()

initial_steps = (UiTestStep(user_input=CLI, comment="ansible-navigator config command top window"),)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
