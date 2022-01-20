"""Tests for ``config`` from CLI, interactive, with an EE.
"""
import pytest

from .base import BaseClass
from .base import base_steps
from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id

CLI = Command(subcommand="config", execution_environment=True).join()

initial_steps = (Step(user_input=CLI, comment="ansible-navigator config command top window"),)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
