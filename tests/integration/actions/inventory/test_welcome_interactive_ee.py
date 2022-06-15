"""Tests for inventory from welcome, interactive, with an EE."""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from .base import base_steps


CLI = Command(execution_environment=True).join()
cmdline = f":inventory -i {ANSIBLE_INVENTORY_FIXTURE_DIR}"

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(user_input=cmdline, comment="ansible-navigator inventory command top window"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
