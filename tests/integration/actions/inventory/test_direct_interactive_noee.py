"""Tests for inventory from CLI, interactive, without an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from .base import base_steps


cmdline = f"-i {ANSIBLE_INVENTORY_FIXTURE_DIR}"
CLI = Command(subcommand="inventory", cmdline=cmdline, execution_environment=False).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="ansible-navigator inventory command top window"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
