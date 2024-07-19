"""Tests for templar from CLI, interactive, with an EE, check {{ readme }}."""

import pytest

from tests.integration._interactions import Command
from tests.integration._interactions import UiTestStep
from tests.integration._interactions import add_indices
from tests.integration._interactions import step_id

from .base import BaseClass


CLI = Command(subcommand="collections", execution_environment=True).join()

steps: tuple[UiTestStep, ...] = (
    UiTestStep(
        user_input=CLI,
        comment="ansible-navigator collections",
        present=["ansible.builtin", "ansible.posix"],
    ),
    UiTestStep(
        user_input=":f ansible.posix",
        comment="filter collections",
        present=["ansible.posix"],
    ),
    UiTestStep(
        user_input=":0",
        comment="select ansible.posix",
    ),
    UiTestStep(user_input=":f", comment="unfiltered", present=["csh"]),
    UiTestStep(user_input=":f csh", comment="filter content", present=["csh"]),
    UiTestStep(
        user_input=":0",
        comment="select csh",
        present=["full_name: ansible.posix.csh"],
    ),
    UiTestStep(
        user_input=":{{ full_name }}",
        comment="open full_name",
        present=["ansible.posix.csh"],
    ),
)

steps = add_indices(steps)


@pytest.mark.parametrize("step", steps, ids=step_id)
class Test(BaseClass):
    """Run the tests for templar from CLI, interactive, with an EE, check {{ readme }}."""

    UPDATE_FIXTURES = False
