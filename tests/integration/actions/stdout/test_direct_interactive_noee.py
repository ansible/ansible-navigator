"""Tests for ``stdout`` from CLI, interactive, without an EE.
"""
import pytest

from .base import ANSIBLE_PLAYBOOK
from .base import BaseClass


CLI = "ansible-navigator" f" run {ANSIBLE_PLAYBOOK}" " --execution-environment false"

testdata = [
    (0, CLI, "run top window", "SUCCESSFUL"),
    (1, ":st", "Check stdout", ":help help"),
    (2, ":back", "Return to play list", ":help help"),
    (3, ":stdout", "Check stdout", ":help help"),
    (4, ":back", "Return to playlist", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """Run the tests for ``stdout`` from CLI, ``interactive``, without an EE."""

    UPDATE_FIXTURES = False
