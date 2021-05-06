""" from welcome interactive w/ ee
"""
from typing import List

import pytest

from .base import BaseClass

from ..._common import container_runtime_or_fail
from ..._common import get_executable_path

# module doc
CLI_MODULE_DOC = (
    get_executable_path("python") + " -m ansible_navigator"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_module_doc: List = [
    (0, CLI_MODULE_DOC, "welcome", "module_doc_pass", []),
    (1, ":doc testorg.coll_1.mod_1", "load doc", "module_doc_pass", []),
    (2, ":{{ examples }}", "load examples", "module_doc_pass", []),
]

# lookup plugin doc
CLI_LOOKUP_DOC = (
    get_executable_path("python") + " -m ansible_navigator"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_lookup_doc: List = [
    (0, CLI_LOOKUP_DOC, "welcome", "lookup_doc_pass", []),
    (1, ":doc testorg.coll_1.lookup_1 -t lookup", "load doc", "lookup_doc_pass", []),
]

# plugin does not exist
CLI_WRONG_MODULE_NOT_EXIST = (
    get_executable_path("python") + " -m ansible_navigator"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_module_doc_not_exist = [
    (0, CLI_WRONG_MODULE_NOT_EXIST, "welcome", "module_doc_fail", []),
    (
        1,
        ":doc testorg.coll_1.doesnotexist",
        "ansible-navigator doc wrong plugin name",
        "module_doc_fail",
        ["module testorg.coll_1.doesnotexist not found in", "execution_environment_errors"],
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
