"""Tests for stdout from welcome, interactive, without an EE."""

import pytest

from tests.integration._interactions import UiTestStep

from .base import ANSIBLE_PLAYBOOK
from .base import BaseClass


CLI = "ansible-navigator --execution-environment false welcome"

steps = (
    UiTestStep(user_input=CLI, comment="welcome screen", step_index=0),
    UiTestStep(
        user_input=f":run {ANSIBLE_PLAYBOOK}",
        comment="Play list",
        present=["Successful"],
        step_index=1,
    ),
    UiTestStep(
        user_input=":st",
        comment="Check stdout",
        step_index=2,
        present=[
            "No inventory was parsed, only implicit localhost is available",
            "TASK [debug]",
            "PLAY RECAP",
        ],
    ),
    UiTestStep(user_input=":back", comment="Return to play list", step_index=3),
    UiTestStep(
        user_input=":stdout",
        comment="Check stdout",
        step_index=4,
        present=[
            "provided hosts list is empty, only localhost is available",
            "ok: [localhost] => (item=1) =>",
            "PLAY RECAP",
        ],
    ),
    UiTestStep(
        user_input=":back", comment="Return to playlist", step_index=4, present=["Successful"]
    ),
)


@pytest.mark.parametrize("step", steps)
class Test(BaseClass):
    """Run the tests for stdout from welcome, interactive, without an EE."""

    UPDATE_FIXTURES = False
