"""Tests for templar from welcome, interactive, with an EE.
"""
import pytest

from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id
from .base import BaseClass
from .base import base_steps
from .base import inventory_path
from .base import playbook_path


CLI = Command(execution_environment=True).join()
cmdline = f":run {playbook_path} -i {inventory_path}"

initial_steps = (
    Step(user_input=CLI, comment="welcome screen"),
    Step(
        user_input=cmdline,
        comment="ansible-navigator run playbook",
        search_within_response=["COMPLETE", "SUCCESSFUL"],
    ),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for templar from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
