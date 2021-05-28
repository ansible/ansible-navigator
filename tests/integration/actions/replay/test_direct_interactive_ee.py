"""direct from cli interactive w/ ee
"""
import pytest

from .base import BaseClass
from .base import PLAYBOOK_ARTIFACT


CLI = "ansible-navigator" f" replay {PLAYBOOK_ARTIFACT}" " --execution-environment true --ll debug"

testdata = [
    (0, CLI, "run top window", ["COMPLETE", "SUCCESSFUL"]),
    (1, ":0", "Task list", ":help help"),
    (2, ":0", "Task 1", ":help help"),
    (3, ":stdout", "Check stdout", ":help help"),
    (4, ":back", "Return to task 1", ":help help"),
    (5, ":back", "Return to task list", ":help help"),
    (6, ":back", "Return to play list", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
