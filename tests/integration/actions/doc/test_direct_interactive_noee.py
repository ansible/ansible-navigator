"""Tests for doc from CLI, interactive, without an EE.
"""

from typing import List

import pytest

from .base import BaseClass


# module doc
CLI_MODULE_DOC = "ansible-navigator doc company_name.coll_1.mod_1 --execution-environment false"
testdata_module_doc: List = [
    (0, CLI_MODULE_DOC, "ansible-navigator doc module plugin display", "module_doc_pass", []),
    (1, ":{{ examples }}", "load examples", "module_doc_pass", []),
]

# lookup plugin doc
CLI_LOOKUP_DOC = (
    "ansible-navigator doc company_name.coll_1.lookup_1 -t lookup --execution-environment false"
)
testdata_lookup_doc: List = [
    (0, CLI_LOOKUP_DOC, "ansible-navigator doc lookup plugin display", "lookup_doc_pass", []),
]

# plugin does not exist
CLI_WRONG_MODULE_NOT_EXIST = (
    "ansible-navigator doc company_name.coll_1.doesnotexist --execution-environment false"
)
testdata_module_doc_not_exist = [
    (
        0,
        CLI_WRONG_MODULE_NOT_EXIST,
        "ansible-navigator doc wrong plugin name",
        "module_doc_fail",
        ["module company_name.coll_1.doesnotexist not found in", "local_errors"],
    ),
]


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output",
    testdata_module_doc,
)
class TestModuleDoc(BaseClass):
    """Run the tests for doc from CLI, interactive, without an EE."""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output",
    testdata_lookup_doc,
)
class TestLookUpDoc(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output",
    testdata_module_doc_not_exist,
)
class TestModuleDocNotExist(BaseClass):
    """run the tests"""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
