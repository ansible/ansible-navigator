""" config direct from cli interactive w/o ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_INVENTORY_FIXTURE_DIR

from ..._common import get_executable_path

CLI = (
    get_executable_path("python") + " -m ansible_navigator inventory"
    " --execution-environment false" + f" -i {ANSIBLE_INVENTORY_FIXTURE_DIR}"
)

testdata = [
    (0, CLI, "ansible-navigator inventory command top window"),
    (1, ":0", "Browse hosts/ungrouped window"),
    (2, ":0", "Group list window"),
    (3, ":0", "group01 hosts detail window"),
    (4, ":0", "host0101 detail window"),
    (5, ":back", "Previous window (group01 hosts detail window)"),
    (6, ":back", "Previous window (Group list window)"),
    (7, ":1", "group02 hosts detail window"),
    (8, ":0", "host0201 detail window"),
    (9, ":back", "Previous window (group02 hosts detail window)"),
    (10, ":back", "Previous window (Group list window)"),
    (11, ":2", "group03 hosts detail window"),
    (12, ":0", "host0301 detail window"),
    (13, ":back", "Previous window (group03 hosts detail window)"),
    (14, ":back", "Previous window (Group list window)"),
    (15, ":back", "Previous window (Browse hosts/ungrouped window)"),
    (16, ":back", "Previous window (top window)"),
    (17, ":1", "Inventory hostname window"),
    (18, ":0", "host0101 detail window"),
    (19, ":back", "Previous window after host0101 (Inventory hostname window)"),
    (20, ":1", "host0201 detail window"),
    (21, ":back", "Previous window after host0201 (Inventory hostname window)"),
    (22, ":2", "host0301 detail window"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
