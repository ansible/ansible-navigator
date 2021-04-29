""" doc direct from cli interactive w/ ee
"""
import pytest

from typing import List
from .base import BaseClass

from ..._common import container_runtime_or_fail
from ..._common import get_executable_path

# module doc
CLI_MODULE_DOC = (
    get_executable_path("python") + " -m ansible_navigator doc testorg.coll_1.mod_1"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_module_doc: List = [
    (0, CLI_MODULE_DOC, "ansible-navigator doc module plugin display", "module_doc_pass", []),
]

# lookup plugin doc
CLI_LOOKUP_DOC = (
    get_executable_path("python") + " -m ansible_navigator doc testorg.coll_1.lookup_1 -t lookup"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_lookup_doc: List = [
    (0, CLI_LOOKUP_DOC, "ansible-navigator doc lookup plugin display", "lookup_doc_pass", []),
]

# plugin does not exist
CLI_WRONG_MODULE_NOT_EXIST = (
    get_executable_path("python") + " -m ansible_navigator doc testorg.coll_1.doesnotexist"
    " --execution-environment true --ce " + container_runtime_or_fail()
)

testdata_module_doc_not_exist = [
    (
        0,
        CLI_WRONG_MODULE_NOT_EXIST,
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

    pass
