""" doc from welcome interactive w/o ee
"""
import pytest

from typing import List
from .base import BaseClass

from ..._common import get_executable_path

# module doc
CLI_WELCOME_SCREEN = get_executable_path("python") + " -m ansible_navigator"
test_module_doc_pass = "module_doc_pass"
testdata_module_doc: List = [
    (0, CLI_WELCOME_SCREEN, "ansible-navigator welcome screen", test_module_doc_pass, []),
    (1, ":doc testorg.coll_1.mod_1", "move to module doc screen", test_module_doc_pass, []),
]

# lookup plugin doc
test_lookup_doc_pass = "lookup_doc_pass"
testdata_lookup_doc: List = [
    (0, CLI_WELCOME_SCREEN, "ansible-navigator welcome screen", test_lookup_doc_pass, []),
    (
        1,
        ":doc testorg.coll_1.lookup_1 -t lookup",
        "move to lookup plugin doc screen",
        test_lookup_doc_pass,
        [],
    ),
]

# plugin does not exist
test_module_doc_fail = "module_doc_fail"
testdata_module_doc_not_exist = [
    (0, CLI_WELCOME_SCREEN, "ansible-navigator welcome screen", test_module_doc_fail, []),
    (
        1,
        ":doc testorg.coll_1.doesnotexist",
        "move to plugin doc error screen",
        test_module_doc_fail,
        ["module testorg.coll_1.doesnotexist not found in", "local_errors"],
    ),
]


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output", testdata_module_doc
)
class TestModuleDoc(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output", testdata_lookup_doc
)
class TestLookUpDoc(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output", testdata_module_doc_not_exist
)
class TestModuleDocNotExist(BaseClass):
    """run the tests"""

    UPDATE_FIXTURES = False
