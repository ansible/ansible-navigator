""" from welcome interactive w/ ee
"""
import pytest

from .base import BaseClass
from .base import PLAYBOOK_ARTIFACT

from ..._common import container_runtime_or_fail

CLI = "ansible-navigator --execution-environment true --ce " + container_runtime_or_fail()


testdata = [
    (0, CLI, "welcome", ":help help"),
    (1, f":load {PLAYBOOK_ARTIFACT}", "Play list", "SUCCESSFUL"),
    (2, ":0", "Task list", ":help help"),
    (3, ":0", "Task 1", ":help help"),
    (4, ":stdout", "Check stdout", ":help help"),
    (5, ":back", "Return to task 1", ":help help"),
    (6, ":back", "Return to task list", ":help help"),
    (7, ":back", "Return to play list", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
