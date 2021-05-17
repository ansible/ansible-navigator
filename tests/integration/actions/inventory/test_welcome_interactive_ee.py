""" inventory from welcome interactive w/ ee
"""
import pytest

from .base import BaseClass
from .base import ANSIBLE_INVENTORY_FIXTURE_DIR

from ...._common import container_runtime_or_fail

CLI = "ansible-navigator --ee True --ce " + container_runtime_or_fail()

testdata = [
    (0, CLI, "ansible-navigator inventory command top window"),
    (1, f":i -i {ANSIBLE_INVENTORY_FIXTURE_DIR}", ":inventory from welcome"),
    (2, ":0", "Browse hosts/ungrouped window"),
    (3, ":0", "Group list window"),
    (4, ":0", "group01 hosts detail window"),
    (5, ":0", "host0101 detail window"),
    (6, ":back", "Previous window (group01 hosts detail window)"),
    (7, ":back", "Previous window (Group list window)"),
    (8, ":1", "group02 hosts detail window"),
    (9, ":0", "host0201 detail window"),
    (10, ":back", "Previous window (group02 hosts detail window)"),
    (11, ":back", "Previous window (Group list window)"),
    (12, ":2", "group03 hosts detail window"),
    (13, ":0", "host0301 detail window"),
    (14, ":back", "Previous window (group03 hosts detail window)"),
    (15, ":back", "Previous window (Group list window)"),
    (16, ":back", "Previous window (Browse hosts/ungrouped window)"),
    (17, ":back", "Previous window (top window)"),
    (18, ":1", "Inventory hostname window"),
    (19, ":0", "host0101 detail window"),
    (20, ":back", "Previous window after host0101 (Inventory hostname window)"),
    (21, ":1", "host0201 detail window"),
    (22, ":back", "Previous window after host0201 (Inventory hostname window)"),
    (23, ":2", "host0301 detail window"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
