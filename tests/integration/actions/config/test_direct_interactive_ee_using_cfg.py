"""Tests for ``config`` from CLI, interactive, with an EE and ansible.cfg file."""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import TEST_FIXTURE_DIR
from .base import BaseClass


CLI = Command(
    subcommand="config",
    execution_environment=True,
    precommand=f"cd {TEST_FIXTURE_DIR}/using_ansible_cfg && ",
).join()

initial_steps = (
    UiTestStep(user_input=CLI, comment="ansible-navigator config command top window"),
    UiTestStep(
        user_input=":0",
        comment="Action warnings",
        present=["current_config_file", "ansible.cfg"],
    ),
)

steps = add_indices(initial_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``config`` from CLI, interactive, with an EE and ansible.cfg file."""

    UPDATE_FIXTURES = False
