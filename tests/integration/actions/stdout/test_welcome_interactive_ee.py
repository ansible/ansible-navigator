"""Tests for stdout from welcome, interactive, with an EE."""

import pytest

from tests.integration._interactions import UiTestStep

from .base import ANSIBLE_PLAYBOOK
from .base import BaseClass


CLI = "ansible-navigator --execution-environment true"

steps = (
    UiTestStep(
        user_input=CLI, comment="welcome screen", step_index=0, search_within_response=":help help"
    ),
    UiTestStep(
        user_input=f":run {ANSIBLE_PLAYBOOK}",
        comment="Play list",
        step_index=1,
        search_within_response="Successful",
    ),
    UiTestStep(
        user_input=":st",
        comment="Check stdout",
        step_index=2,
        search_within_response=":help help",
        present=["PLAY RECAP"],
    ),
    UiTestStep(
        user_input=":back",
        comment="Return to play list",
        step_index=3,
        search_within_response=":help help",
        present=["Complete", "Successful"],
    ),
    UiTestStep(
        user_input=":stdout",
        comment="Check stdout",
        step_index=4,
        search_within_response=":help help",
        present=["PLAY RECAP", "TASK [debug]"],
    ),
    UiTestStep(
        user_input=":back",
        comment="Return to playlist",
        step_index=5,
        search_within_response=":help help",
        present=["Complete", "Successful"],
    ),
)


@pytest.mark.parametrize("step", steps)
class Test(BaseClass):
    """Run the tests for stdout from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
