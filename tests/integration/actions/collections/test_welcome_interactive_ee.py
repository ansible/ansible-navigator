""" collections from welcome interactive w/0 ee
"""
import pytest

from .base import BaseClass
from ..._common import container_runtime_or_fail


CLI = "ansible-navigator --execution-environment true --ce " + container_runtime_or_fail()

testdata = [
    (0, CLI, "ansible-navigator welcome screen", None),
    (
        1,
        ":collections",
        "ansible-navigator collections top window",
        "Collecting collection content",
    ),
    (2, ":0", "Browse testorg.coll_1 plugins window", None),
    (3, ":0", "lookup_1 plugin docs window", None),
    (4, ":back", "Back to browse testorg.coll_1 plugins window", None),
    (5, ":1", "mod_1 plugin docs window", None),
    (6, ":back", "Back to browse testorg.coll_1 plugins window", None),
    (7, ":back", "Back to ansible-navigator collections browse window", None),
    (8, ":1", "Browse testorg.coll_2 plugins window", None),
    (9, ":0", "lookup_2 plugin docs window", None),
    (10, ":back", "Back to browse testorg.coll_2 plugins window", None),
    (11, ":1", "mod_2 plugin docs window", None),
    (12, ":back", "Back to browse testorg.coll_2 plugins window", None),
    (13, ":back", "Back to ansible-navigator collections browse window", None),
]


@pytest.mark.parametrize("index, user_input, comment, collection_fetch_prompt", testdata)
class Test(BaseClass):
    """run the tests"""

    EXECUTION_ENVIRONMENT_TEST = True
    UPDATE_FIXTURES = False
