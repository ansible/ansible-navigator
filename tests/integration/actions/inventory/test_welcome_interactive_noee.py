"""Tests for inventory from welcome, interactive, without an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id
from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from .base import base_steps


CLI = Command(execution_environment=False).join()
cmdline = f":inventory -i {ANSIBLE_INVENTORY_FIXTURE_DIR}"

initial_steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(user_input=cmdline, comment="ansible-navigator inventory command top window"),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
