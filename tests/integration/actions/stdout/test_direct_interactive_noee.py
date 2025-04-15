"""Tests for ``stdout`` from CLI, interactive, without an EE."""

import pytest

from tests.integration._interactions import UiTestStep

from .base import ANSIBLE_PLAYBOOK
from .base import BaseClass


CLI = f"ansible-navigator run {ANSIBLE_PLAYBOOK} --execution-environment false"


steps = [
    UiTestStep(CLI, comment="run top window", step_index=0, search_within_response="Successful"),
    UiTestStep(
        user_input=":st",
        comment="Check stdout",
        step_index=1,
        search_within_response=":help help",
        present=["PLAY [localhost]", "PLAY RECAP"],
    ),
    UiTestStep(
        user_input=":back",
        comment="Return to play list",
        step_index=2,
        search_within_response=":help help",
    ),
    UiTestStep(
        user_input=":stdout",
        comment="Check stdout",
        step_index=3,
        search_within_response=":help help",
        present=["PLAY RECAP", "TASK [debug]"],
    ),
    UiTestStep(
        user_input=":back",
        comment="Return to playlist",
        step_index=4,
        search_within_response=":help help",
    ),
]


@pytest.mark.parametrize("step", steps)
class Test(BaseClass):
    """Run the tests for ``stdout`` from CLI, ``interactive``, without an EE."""

    UPDATE_FIXTURES = False
