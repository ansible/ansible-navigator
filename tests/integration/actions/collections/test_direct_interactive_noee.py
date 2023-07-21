"""Tests for collections from CLI, interactive, without an EE."""
import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import EXPECTED_COLLECTIONS
from .base import BaseClass
from .base import base_steps


CLI = Command(subcommand="collections", execution_environment=False).join()


initial_steps = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator collections top window",
        present=EXPECTED_COLLECTIONS,
    ),
)

steps = add_indices(initial_steps + base_steps)


@pytest.mark.parametrize("step", steps, ids=step_id_padded)
class Test(BaseClass):
    """Run the tests for ``collections`` from CLI, interactive, without an EE."""

    update_fixtures = False
