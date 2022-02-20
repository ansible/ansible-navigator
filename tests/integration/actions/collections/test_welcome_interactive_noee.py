"""Tests for collections from welcome, interactive, without an EE.
"""
import pytest

from .base import BaseClass


CLI = "ansible-navigator --execution-environment false"

testdata = [
    (0, CLI, "ansible-navigator welcome screen"),
    (1, ":collections", "ansible-navigator collections top window"),
    (2, ":0", "Browse company_name.coll_1 plugins window"),
    (3, ":0", "lookup_1 plugin docs window"),
    (4, ":back", "Back to browse company_name.coll_1 plugins window"),
    (5, ":1", "mod_1 plugin docs window"),
    (6, ":back", "Back to browse company_name.coll_1 plugins window"),
    (7, ":back", "Back to ansible-navigator collections browse window"),
    (8, ":1", "Browse company_name.coll_2 plugins window"),
    (9, ":0", "lookup_2 plugin docs window"),
    (10, ":back", "Back to browse company_name.coll_2 plugins window"),
    (11, ":1", "mod_2 plugin docs window"),
    (12, ":back", "Back to browse company_name.coll_2 plugins window"),
    (13, ":back", "Back to ansible-navigator collections browse window"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """Run the tests for collections from welcome, interactive, without an EE."""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
