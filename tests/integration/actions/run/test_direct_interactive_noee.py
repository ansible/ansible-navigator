"""Tests for run from CLI, interactive, without an EE."""
import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import BaseClass
from .base import base_steps
from .base import inventory_path
from .base import playbook_path


cmdline = f"{playbook_path} -i {inventory_path}"
CLI = Command(subcommand="run", cmdline=cmdline, execution_environment=False).join()

initial_steps = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator run playbook",
        search_within_response=["Complete", "Successful"],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for run from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
