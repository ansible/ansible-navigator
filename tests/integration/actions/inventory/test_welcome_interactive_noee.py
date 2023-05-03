"""Tests for inventory from welcome, interactive, without an EE."""
import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from .base import base_steps


CLI = Command(execution_environment=False).join()
cmdline = f":inventory -i {ANSIBLE_INVENTORY_FIXTURE_DIR}"

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(user_input=cmdline, comment="ansible-navigator inventory command top window"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
