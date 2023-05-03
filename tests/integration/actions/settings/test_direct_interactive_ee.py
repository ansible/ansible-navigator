"""Tests for ``settings`` from CLI, interactive, with an EE."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id

from .base import BaseClass
from .base import base_steps


CLI = Command(subcommand="settings", execution_environment=True).join()

initial_steps = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator settings command top window",
        present=["Ansible runner artifact dir", "Help config"],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for ``settings`` from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
