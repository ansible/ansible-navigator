""" inventory integration tests
"""
import json
import os
import pytest

from ... import defaults
from .._common import get_executable_path
from .._common import fixture_path_from_request
from .._common import update_fixtures  # pylint: disable=unused-import


CLI = (
    f"{get_executable_path('python')}"
    " -m ansible_navigator inventory"
    f" -i {os.path.join(defaults.FIXTURES_DIR,'inventory')}"
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


def test_testdata_indicies():
    """sanity check on the data because I forgot how to count"""
    expected = list(range(0, len(testdata)))
    actual = [x[0] for x in testdata]
    assert expected == actual


@pytest.mark.parametrize("index, user_input, comment", testdata)
def test_inventory_interactive_inventory_list(request, tmux_session, index, user_input, comment):
    # pylint:disable=unused-argument
    """test interactive inventory

    uncomment the update_fixtures line to update the fixtures
    """
    received_output = tmux_session.interaction(user_input)
    # update_fixtures(request, index, received_output, comment) # FIXME: keep commented out
    dir_path, file_name = fixture_path_from_request(request, index)
    with open(f"{dir_path}/{file_name}") as infile:
        expected_output = json.load(infile)["output"]
    assert expected_output == received_output
