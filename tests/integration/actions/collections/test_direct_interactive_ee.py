""" collections direct from cli interactive with ee
"""
import pytest

from .base import BaseClass

from ..._common import container_runtime_or_fail


CLI = (
    "ansible-navigator collections --execution-environment true --ce " + container_runtime_or_fail()
)

testdata = [
    (0, CLI, "ansible-navigator collections browse window", "Collecting collection content"),
    (1, ":0", "Browse testorg.coll_1 plugins window", None),
    (2, ":0", "lookup_1 plugin docs window", None),
    (3, ":back", "Back to browse testorg.coll_1 plugins window", None),
    (4, ":1", "mod_1 plugin docs window", None),
    (5, ":back", "Back to browse testorg.coll_1 plugins window", None),
    (6, ":back", "Back to ansible-navigator collections browse window", None),
    (7, ":1", "Browse testorg.coll_2 plugins window", None),
    (8, ":0", "lookup_2 plugin docs window", None),
    (9, ":back", "Back to browse testorg.coll_2 plugins window", None),
    (10, ":1", "mod_2 plugin docs window", None),
    (11, ":back", "Back to browse testorg.coll_2 plugins window", None),
    (12, ":back", "Back to ansible-navigator collections browse window", None),
]


@pytest.mark.parametrize("index, user_input, comment, collection_fetch_prompt", testdata)
class Test(BaseClass):
    """run the tests"""

    EXECUTION_ENVIRONMENT_TEST = True
    UPDATE_FIXTURES = False
