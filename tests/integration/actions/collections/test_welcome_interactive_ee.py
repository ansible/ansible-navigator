""" collections from welcome interactive w/0 ee
"""
import pytest

from .base import BaseClass
from ..._common import container_runtime_or_fail


CLI = "ansible-navigator --execution-environment true --ce " + container_runtime_or_fail()

testdata = [
    (0, CLI, "ansible-navigator welcome screen"),
    (1, ":collections", "ansible-navigator collections top window"),
    (2, ":0", "Browse testorg.coll_1 plugins window"),
    (3, ":0", "lookup_1 plugin docs window"),
    (4, ":back", "Back to browse testorg.coll_1 plugins window"),
    (5, ":1", "mod_1 plugin docs window"),
    (6, ":back", "Back to browse testorg.coll_1 plugins window"),
    (7, ":back", "Back to ansible-navigator collections browse window"),
    (8, ":1", "Browse testorg.coll_2 plugins window"),
    (9, ":0", "lookup_2 plugin docs window"),
    (10, ":back", "Back to browse testorg.coll_2 plugins window"),
    (11, ":1", "mod_2 plugin docs window"),
    (12, ":back", "Back to browse testorg.coll_2 plugins window"),
    (13, ":back", "Back to ansible-navigator collections browse window"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    EXECUTION_ENVIRONMENT_TEST = True
    UPDATE_FIXTURES = False
