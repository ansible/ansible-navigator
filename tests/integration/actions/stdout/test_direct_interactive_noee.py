""" direct from cli interactive w/o ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_PLAYBOOK


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
    """run the tests"""

    UPDATE_FIXTURES = False
