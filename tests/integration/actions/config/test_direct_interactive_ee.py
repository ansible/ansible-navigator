""" config direct from cli interactive w/ ee
"""
import pytest

from .base import BaseClass

from ..._common import get_executable_path
from ..._common import container_runtime_or_fail

CLI = (
<<<<<<< HEAD
    get_executable_path("python")
    + " -m ansible_navigator config --execution-environment true --ce "
    + container_runtime_or_fail()
=======
    f"{get_executable_path('python')}"
    f" -m ansible_navigator config --execution-environment true --ce {container_runtime_or_fail()}"
>>>>>>> 43dbf77b9b84aa2b1d58382581671a7f16f36660
)

testdata = [
    (0, CLI, "ansible-navigator config command top window"),
    (1, ":f CACHE_PLUGIN_TIMEOUT", "filter for cache plugin timeout"),
    (2, ":0", "cache plugin details"),
    (3, ":back", "return to filtered list"),
    (4, ":f", "clear filter, full list"),
    (5, ":f yaml", "filter off screen value"),
    (6, ":3", "YAML_FILENAME_EXTENSIONS details"),
    (7, ":back", "return to filtered list"),
    (8, ":f", "clear filter, full list"),
]


@pytest.mark.parametrize("index, user_input, comment", testdata)
class Test(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
