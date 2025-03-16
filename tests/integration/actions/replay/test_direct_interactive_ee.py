"""Tests for replay from CLI, interactive, with an EE."""

import pytest

from .base import PLAYBOOK_ARTIFACT
from .base import BaseClass


CLI = f"ansible-navigator replay {PLAYBOOK_ARTIFACT} --execution-environment true --ll debug"

testdata = [
    pytest.param(0, CLI, "run top window", ["Complete", "Successful"], id="0"),
    pytest.param(1, ":0", "Task list", ":help help", id="1"),
    pytest.param(2, ":0", "Task 1", ":help help", id="2"),
    pytest.param(3, ":stdout", "Check stdout", ":help help", id="3"),
    pytest.param(4, ":back", "Return to task 1", ":help help", id="4"),
    pytest.param(5, ":back", "Return to task list", ":help help", id="5"),
    pytest.param(6, ":back", "Return to play list", ":help help", id="6"),
]


@pytest.mark.parametrize(("index", "user_input", "comment", "search_within_response"), testdata)
class Test(BaseClass):
    """Run the tests for replay from CLI, interactive, with an EE."""

    UPDATE_FIXTURES = False
