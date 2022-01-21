"""Tests for replay from welcome, interactive, with an EE.
"""
import pytest

from .base import PLAYBOOK_ARTIFACT
from .base import BaseClass


CLI = "ansible-navigator --execution-environment true"


testdata = [
    (0, CLI, "welcome", ":help help"),
    (1, f":replay {PLAYBOOK_ARTIFACT}", "Play list", ["COMPLETE", "SUCCESSFUL"]),
    (2, ":0", "Task list", ":help help"),
    (3, ":0", "Task 1", ":help help"),
    (4, ":stdout", "Check stdout", ":help help"),
    (5, ":back", "Return to task 1", ":help help"),
    (6, ":back", "Return to task list", ":help help"),
    (7, ":back", "Return to play list", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """Run the tests for images from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
