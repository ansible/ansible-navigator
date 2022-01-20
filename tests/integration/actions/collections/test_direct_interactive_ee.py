"""Tests for collections from CLI, interactive, with an EE.
"""
import pytest

from .base import BaseClass


CLI = "ansible-navigator collections --execution-environment true"

testdata = [
    (0, CLI, "ansible-navigator collections browse window"),
    (1, ":0", "Browse testorg.coll_1 plugins window"),
    (2, ":0", "lookup_1 plugin docs window"),
    (3, ":back", "Back to browse testorg.coll_1 plugins window"),
    (4, ":1", "mod_1 plugin docs window"),
    (5, ":back", "Back to browse testorg.coll_1 plugins window"),
    (6, ":back", "Back to ansible-navigator collections browse window"),
    (7, ":1", "Browse testorg.coll_2 plugins window"),
    (8, ":0", "lookup_2 plugin docs window"),
    (9, ":back", "Back to browse testorg.coll_2 plugins window"),
    (10, ":1", "mod_2 plugin docs window"),
    (11, ":back", "Back to browse testorg.coll_2 plugins window"),
    (12, ":back", "Back to ansible-navigator collections browse window"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    # pylint: disable=too-few-public-methods
    """Run the tests for collections from CLI, interactive, with an EE."""

    TEST_FOR_MODE = "interactive"
    EXECUTION_ENVIRONMENT_TEST = True
    UPDATE_FIXTURES = False
