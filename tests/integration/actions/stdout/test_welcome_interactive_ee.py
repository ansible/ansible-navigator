"""Tests for stdout from welcome, interactive, with an EE."""

import pytest

from .base import ANSIBLE_PLAYBOOK
from .base import BaseClass


CLI = "ansible-navigator --execution-environment true"

testdata = [
    pytest.param(0, CLI, "welcome", ":help help", id="0"),
    pytest.param(1, f":run {ANSIBLE_PLAYBOOK}", "Play list", "Successful", id="1"),
    pytest.param(2, ":st", "Check stdout", ":help help", id="2"),
    pytest.param(3, ":back", "Return to play list", ":help help", id="3"),
    pytest.param(4, ":stdout", "Check stdout", ":help help", id="4"),
    pytest.param(5, ":back", "Return to playlist", ":help help", id="5"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """Run the tests for stdout from welcome, interactive, with an EE."""

    UPDATE_FIXTURES = False
