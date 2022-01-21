"""Tests for templar from CLI, interactive, without an EE.
"""
import pytest

from .base import BaseClass
from .base import base_steps
from .base import inventory_path
from .base import playbook_path
from ..._interactions import Command
from ..._interactions import Step
from ..._interactions import add_indicies
from ..._interactions import step_id


cmdline = f"{playbook_path} -i {inventory_path}"
CLI = Command(subcommand="run", cmdline=cmdline, execution_environment=False).join()

initial_steps = (
    Step(
        user_input=CLI,
        comment="ansible-navigator run playbook",
        search_within_response=["COMPLETE", "SUCCESSFUL"],
    ),
)

steps = add_indicies(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for templar from CLI, interactive, without an EE."""

    UPDATE_FIXTURES = False
