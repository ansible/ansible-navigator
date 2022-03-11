"""Tests for ``settings`` from CLI, interactive, with an EE."""

import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import BaseClass
from .base import base_steps


CLI = Command(subcommand="settings", execution_environment=True).join()

initial_steps = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator settings command top window",
        present=["Ansible runner artifact dir", "Help playbook"],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``settings`` from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
