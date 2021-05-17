""" config direct from cli interactive w/ ee
"""
import pytest

from .base import BaseClass

from ...._common import container_runtime_or_fail

CLI = "ansible-navigator config --execution-environment true --ce " + container_runtime_or_fail()

testdata = [
    (0, CLI, "ansible-navigator config command top window", None, None),
    (1, ":f CACHE_PLUGIN_TIMEOUT", "filter for cache plugin timeout", None, None),
    (2, ":0", "cache plugin details", None, None),
    (3, ":back", "return to filtered list", None, None),
    (4, ":f", "clear filter, full list", None, None),
    (5, ":f yaml", "filter off screen value", None, None),
    (6, ":3", "YAML_FILENAME_EXTENSIONS details", None, None),
    (7, ":back", "return to filtered list", None, None),
    (8, ":f", "clear filter, full list", None, None),
]


@pytest.mark.parametrize("index, user_input, comment, testname, expected_in_output", testdata)
class Test(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
