"""direct from cli interactive w/ ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_PLAYBOOK

from ..._common import get_executable_path
from ..._common import container_runtime_or_fail

CLI = (
    get_executable_path("python") + " -m ansible_navigator"
    f" run {ANSIBLE_PLAYBOOK}"
    " --execution-environment true --ll debug --ce " + container_runtime_or_fail()
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
