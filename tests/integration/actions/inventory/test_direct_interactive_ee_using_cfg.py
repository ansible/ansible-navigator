"""Tests for inventory from CLI, interactive, with an EE, using ansible.cfg."""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import TEST_FIXTURE_DIR
from .base import BaseClass


CLI = Command(
    subcommand="inventory",
    execution_environment=True,
    precommand=f"cd {TEST_FIXTURE_DIR}/using_ansible_cfg && ",
).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="ansible-navigator inventory command top window"),
    UiTestStep(
        user_input=":1",
        comment="visit host from inventory specified in ansible.cfg",
        present=["from.ansible.cfg"],
    ),
)

steps = add_indices(initial_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, with an EE, using ansible.cfg."""

    UPDATE_FIXTURES = False
