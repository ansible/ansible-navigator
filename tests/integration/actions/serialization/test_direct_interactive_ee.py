"""Tests for serialization from CLI, interactive, with an EE."""
import pytest

from ..._interactions import Command
from ..._interactions import add_indices
from ..._interactions import step_id_padded
from .base import BaseClass
from .base import SerUiTestStep
from .base import base_steps


CLI = Command(subcommand="collections", execution_environment=True).join()


initial_steps = (SerUiTestStep(user_input=CLI, comment="ansible-navigator collections top window"),)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for serialization from CLI, interactive, with an EE."""

    update_fixtures = False