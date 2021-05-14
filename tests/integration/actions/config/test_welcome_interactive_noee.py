""" config from welcome interactive w ee
"""
import pytest

from .base import BaseClass

CLI = "ansible-navigator --execution-environment false"

testdata = [
    (0, CLI, "ansible-navigator config command top window", None, None),
    (1, ":config", "enter config from welcome screen", None, None),
    (2, ":f CACHE_PLUGIN_TIMEOUT", "filter for cache plugin timeout", None, None),
    (3, ":0", "cache plugin details", None, None),
    (4, ":back", "return to filtered list", None, None),
    (5, ":f", "clear filter, full list", None, None),
    (6, ":f yaml", "filter off screen value", None, None),
    (7, ":3", "YAML_FILENAME_EXTENSIONS details", None, None),
    (8, ":back", "return to filtered list", None, None),
    (9, ":f", "clear filter, full list", None, None),
]


@pytest.mark.parametrize("index, user_input, comment, testname, expected_in_output", testdata)
class Test(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
