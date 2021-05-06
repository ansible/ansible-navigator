""" from welcome interactive w/ ee
"""
import pytest

from .base import BaseClass
from .base import PLAYBOOK_ARTIFACT

from ..._common import get_executable_path
from ..._common import container_runtime_or_fail

CLI = (
    get_executable_path("python") + " -m ansible_navigator"
    " --execution-environment true --ce " + container_runtime_or_fail()
)


testdata = [
    (0, CLI, "welcome", None),
    (1, f":load {PLAYBOOK_ARTIFACT}", "Play list", "SUCCESSFUL"),
    (2, ":0", "Task list", None),
    (3, ":0", "Task 1", None),
    (4, ":stdout", "Check stdout", None),
    (5, ":back", "Return to task 1", None),
    (6, ":back", "Return to task list", None),
    (7, ":back", "Return to play list", None),
]


@pytest.mark.parametrize("index, user_input, comment, playbook_status", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
