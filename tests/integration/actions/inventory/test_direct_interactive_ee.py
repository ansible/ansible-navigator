"""Tests for inventory from CLI, interactive, with an EE."""
import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import ANSIBLE_INVENTORY_FIXTURE_DIR
from .base import BaseClass
from .base import base_steps


cmdline = f"-i {ANSIBLE_INVENTORY_FIXTURE_DIR}"
CLI = Command(subcommand="inventory", cmdline=cmdline, execution_environment=True).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="ansible-navigator inventory command top window"),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
