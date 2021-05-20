""" run direct from cli interactive with ee
"""
import os
import pytest

from typing import List
from .base import BaseClass
from .base import inventory_path
from .base import playbook_path
from ...._common import container_runtime_or_fail


CLI_RUN = (
    f"ansible-navigator run {playbook_path} -i {inventory_path}"
    + " --ee true --ce "
    + container_runtime_or_fail()
)

testdata_run: List = [
    (0, CLI_RUN, "ansible-navigator run playbook", ["100%", "SUCCESSFUL"]),
    (1, ":0", "play-1 details", ":help help"),
    (2, ":0", "task-1 details", ":help help"),
    (3, ":back", "play-1 details", ":help help"),
    (4, ":1", "play-1 task-2 details", ":help help"),
    (5, ":back", "play-1 details", ":help help"),
    (6, ":back", "all play details", ":help help"),
    (7, ":1", "play-2 details", ":help help"),
    (8, ":0", "play-2 task-1 details", ":help help"),
    (9, ":back", "play-2 details", ":help help"),
    (10, ":1", "play-2 task-2 details", ":help help"),
    (11, ":back", "play-2 details", ":help help"),
    (12, ":back", "all play details", ":help help"),
    (13, ":st", "display stream", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata_run)
class TestDirectRunEe(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
