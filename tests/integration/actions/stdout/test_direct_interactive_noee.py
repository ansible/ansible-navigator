"""Tests for ``stdout`` from CLI, interactive, without an EE."""

import pytest

from .base import ANSIBLE_PLAYBOOK
from .base import BaseClass


CLI = f"ansible-navigator run {ANSIBLE_PLAYBOOK} --execution-environment false"

testdata = [
    pytest.param(0, CLI, "run top window", "Successful", id="0"),
    pytest.param(1, ":st", "Check stdout", ":help help", id="1"),
    pytest.param(2, ":back", "Return to play list", ":help help", id="2"),
    pytest.param(3, ":stdout", "Check stdout", ":help help", id="3"),
    pytest.param(4, ":back", "Return to playlist", ":help help", id="4"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """Run the tests for ``stdout`` from CLI, ``interactive``, without an EE."""

    UPDATE_FIXTURES = False
