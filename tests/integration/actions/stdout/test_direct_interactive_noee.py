""" direct from cli interactive w/o ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_PLAYBOOK

from ..._common import get_executable_path

CLI = (
    get_executable_path("python") + " -m ansible_navigator"
    f" run {ANSIBLE_PLAYBOOK}"
    " --execution-environment false"
)

testdata = [
    (0, CLI, "run top window", "SUCCESSFUL"),
    (1, ":st", "Check stdout", None),
    (2, ":back", "Return to play list", None),
    (3, ":stdout", "Check stdout", None),
    (4, ":back", "Return to playlist", None),
]


@pytest.mark.parametrize("index, user_input, comment, playbook_status", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
