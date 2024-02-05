"""Tests for run from CLI, interactive, no EE, using collection playbook."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id_padded

from .base import PLAYBOOK_COLLECTION
from .base import BaseClass
from .base import base_steps
from .base import common_fixture_dir


cmdline = f"{PLAYBOOK_COLLECTION}"
CLI = Command(
    subcommand="run",
    cmdline=cmdline,
    execution_environment=False,
    precommand=f"ANSIBLE_COLLECTIONS_PATHS={common_fixture_dir}",
).join()

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
    """Run the tests for run from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
