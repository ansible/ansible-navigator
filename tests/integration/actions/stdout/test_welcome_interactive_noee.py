""" from welcome interactive w/o ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_PLAYBOOK


CLI = "ansible-navigator --execution-environment false"

testdata = [
    (0, CLI, "welcome", ":help help"),
    (1, f":run {ANSIBLE_PLAYBOOK}", "Play list", "SUCCESSFUL"),
    (2, ":st", "Check stdout", ":help help"),
    (3, ":back", "Return to play list", ":help help"),
    (4, ":stdout", "Check stdout", ":help help"),
    (5, ":back", "Return to playlist", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
