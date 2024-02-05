"""Tests for run from welcome, interactive, without an EE."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import BaseClass
from .base import base_steps
from .base import inventory_path
from .base import playbook_path


CLI = Command(execution_environment=False).join()
cmdline = f":run {playbook_path} -i {inventory_path}"

initial_steps = (
    UiTestStep(user_input=CLI, comment="welcome screen"),
    UiTestStep(
        user_input=cmdline,
        comment="ansible-navigator run playbook",
        search_within_response=["Complete", "Successful"],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for run from welcome, interactive, without an EE."""

    UPDATE_FIXTURES = False
