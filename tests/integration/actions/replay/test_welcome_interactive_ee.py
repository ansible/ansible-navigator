"""Tests for replay from welcome, interactive, with an EE."""

import pytest

from .base import PLAYBOOK_ARTIFACT
from .base import BaseClass


CLI = "ansible-navigator --execution-environment true"


testdata = [
    pytest.param(0, CLI, "welcome", ":help help", id="0"),
    pytest.param(
        1, f":replay {PLAYBOOK_ARTIFACT}", "Play list", ["Complete", "Successful"], id="1"
    ),
    pytest.param(2, ":0", "Task list", ":help help", id="2"),
    pytest.param(3, ":0", "Task 1", ":help help", id="3"),
    pytest.param(4, ":stdout", "Check stdout", ":help help", id="4"),
    pytest.param(5, ":back", "Return to task 1", ":help help", id="5"),
    pytest.param(6, ":back", "Return to task list", ":help help", id="6"),
    pytest.param(7, ":back", "Return to play list", ":help help", id="7"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """Run the tests for images from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
