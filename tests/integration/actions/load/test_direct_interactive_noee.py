""" direct from cli interactive w/o ee
"""
import pytest

from .base import BaseClass
from .base import PLAYBOOK_ARTIFACT

from ..._common import get_executable_path

CLI = (
    get_executable_path("python") + " -m ansible_navigator"
    f" load {PLAYBOOK_ARTIFACT}"
    " --execution-environment false"
)

testdata = [
    (0, CLI, "run top window", "SUCCESSFUL"),
    (1, ":0", "Task list", None),
    (2, ":0", "Task 1", None),
    (3, ":stdout", "Check stdout", None),
    (4, ":back", "Return to task 1", None),
    (5, ":back", "Return to task list", None),
    (6, ":back", "Return to play list", None),
]


@pytest.mark.parametrize("index, user_input, comment, playbook_status", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
