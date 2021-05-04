""" from welcome interactive w/o ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_PLAYBOOK

from ..._common import get_executable_path

CLI = get_executable_path("python") + " -m ansible_navigator" " --execution-environment false"

testdata = [
    (0, CLI, "welcome", None),
    (1, f":run {ANSIBLE_PLAYBOOK}", "Play list", "SUCCESSFUL"),
    (2, ":st", "Check stdout", None),
    (3, ":back", "Return to play list", None),
    (4, ":stdout", "Check stdout", None),
    (5, ":back", "Return to playlist", None),
]


@pytest.mark.parametrize("index, user_input, comment, playbook_status", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
