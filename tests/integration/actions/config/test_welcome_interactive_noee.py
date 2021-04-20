""" config from welcome interactive w ee
"""
import pytest

from .base import BaseClass

from ..._common import get_executable_path

CLI = f"{get_executable_path('python')}" f" -m ansible_navigator --execution-environment false"

testdata = [
    (0, CLI, "ansible-navigator config command top window"),
    (1, ":config", "enter config from welcome screen"),
    (2, ":f CACHE_PLUGIN_TIMEOUT", "filter for cache plugin timeout"),
    (3, ":0", "cache plugin details"),
    (4, ":back", "return to filtered list"),
    (5, ":f", "clear filter, full list"),
    (6, ":f yaml", "filter off screen value"),
    (7, ":3", "YAML_FILENAME_EXTENSIONS details"),
    (8, ":back", "return to filtered list"),
    (9, ":f", "clear filter, full list"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
