"""Tests for run from CLI, interactive, with an EE, with unicode."""
import pytest

from ..._interactions import Command
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import BaseClass
from .base import base_steps
from .base import inventory_path
from .base import playbook_path


cmdline = f"{playbook_path} -i {inventory_path}"
CLI = Command(subcommand="run", cmdline=cmdline, execution_environment=True).join()

initial_steps = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator run playbook",
        search_within_response=["COMPLETE", "SUCCESSFUL"],
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for run from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
