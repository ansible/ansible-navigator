"""Tests for inventory from CLI, interactive, with an EE, missing inventory."""
import pytest

from ..._interactions import Command
from ..._interactions import SearchFor
from ..._interactions import UiTestStep
from ..._interactions import add_indices
from ..._interactions import step_id
from .base import TEST_FIXTURE_DIR
from .base import BaseClass


initial_steps = (
    UiTestStep(
        user_input=Command(
            subcommand="inventory",
            cmdline="-i not_a_real_inventory.yml",
            execution_environment=True,
            precommand=f"cd {TEST_FIXTURE_DIR}  && ",
        ).join(),
        comment="ansible-navigator inventory command top window",
        present=["Unable to parse"],
        search_within_response=SearchFor.WARNING,
    ),
    UiTestStep(
        user_input="echo exited",
        comment="exit",
        search_within_response=SearchFor.PROMPT,
        present=["exited"],
    ),
    UiTestStep(
        user_input=Command(
            subcommand="inventory",
            cmdline="-i broken_inventory.yml",
            execution_environment=True,
            precommand=f"cd {TEST_FIXTURE_DIR}  && ",
        ).join(),
        comment="ansible-navigator inventory command top window",
        present=["Unable to parse"],
        search_within_response=SearchFor.WARNING,
    ),
    UiTestStep(
        user_input="echo exited",
        comment="exit",
        search_within_response=SearchFor.PROMPT,
        present=["exited"],
    ),
    UiTestStep(
        user_input=Command(
            subcommand="inventory",
            cmdline="-i broken_inventory.ini",
            execution_environment=True,
            precommand=f"cd {TEST_FIXTURE_DIR}  && ",
        ).join(),
        comment="ansible-navigator inventory command top window",
        present=["Unable to parse"],
        search_within_response=SearchFor.WARNING,
    ),
)

steps = add_indices(initial_steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for inventory from CLI, interactive, with an EE, missing inventory."""

    UPDATE_FIXTURES = False
