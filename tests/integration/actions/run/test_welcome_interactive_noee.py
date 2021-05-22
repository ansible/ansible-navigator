""" from welcome interactive without ee
"""
import os
import pytest

from typing import List
from .base import BaseClass
from .base import inventory_path
from .base import playbook_path


CLI = "ansible-navigator --execution-environment false"

testdata_run: List = [
    (0, CLI, "ansible-navigator run command top window", ":help help"),
    (
        1,
        f":run {playbook_path} -i {inventory_path}",
        "enter run from welcome screen",
        ["100%", "SUCCESSFUL"],
    ),
    (2, ":0", "play-1 details", ":help help"),
    (3, ":0", "task-1 details", ":help help"),
    (4, ":back", "play-1 details", ":help help"),
    (5, ":1", "play-1 task-2 details", ":help help"),
    (6, ":back", "play-1 details", ":help help"),
    (7, ":back", "all play details", ":help help"),
    (8, ":1", "play-2 details", ":help help"),
    (9, ":0", "play-2 task-1 details", ":help help"),
    (10, ":back", "play-2 details", ":help help"),
    (11, ":1", "play-2 task-2 details", ":help help"),
    (12, ":back", "play-2 details", ":help help"),
    (13, ":back", "all play details", ":help help"),
    (14, ":st", "display stream", ":help help"),
]


@pytest.mark.parametrize("index, user_input, comment, search_within_response", testdata_run)
class TestWelcomeRunNoee(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
