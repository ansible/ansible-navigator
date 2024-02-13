"""Tests for doc from CLI, interactive, without an EE."""

from __future__ import annotations

import pytest

from .base import BaseClass


# module doc
CLI_MODULE_DOC = "ansible-navigator doc company_name.coll_1.mod_1 --execution-environment false"
testdata_module_doc = [
    pytest.param(
        0,
        CLI_MODULE_DOC,
        "ansible-navigator doc module plugin display",
        "module_doc_pass",
        [],
        id="0",
    ),
    pytest.param(1, ":{{ examples }}", "load examples", "module_doc_pass", [], id="1"),
]

# lookup plugin doc
CLI_LOOKUP_DOC = (
    "ansible-navigator doc company_name.coll_1.lookup_1 -t lookup --execution-environment false"
)
testdata_lookup_doc = [
    pytest.param(
        0,
        CLI_LOOKUP_DOC,
        "ansible-navigator doc lookup plugin display",
        "lookup_doc_pass",
        [],
        id="0",
    ),
]

# filter plugin doc
CLI_FILTER_DOC = (
    "ansible-navigator doc company_name.coll_1.filter_1 -t filter --execution-environment false"
)
testdata_filter_doc = [
    pytest.param(
        0,
        CLI_FILTER_DOC,
        "ansible-navigator doc filter plugin display",
        "filter_doc_pass",
        [],
        id="0",
    ),
]

# plugin does not exist
CLI_WRONG_MODULE_NOT_EXIST = (
    "ansible-navigator doc company_name.coll_1.doesnotexist --execution-environment false"
)
testdata_module_doc_not_exist = [
    pytest.param(
        0,
        CLI_WRONG_MODULE_NOT_EXIST,
        "ansible-navigator doc wrong plugin name",
        "module_doc_fail",
        ["WARNING", "module", "company_name.coll_1.doesnotexist", "not", "found", "local_errors"],
        id="0",
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
    """Run the tests."""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output",
    testdata_filter_doc,
)
class TestFilterDoc(BaseClass):
    """Run the tests."""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False


@pytest.mark.parametrize(
    "index, user_input, comment, testname, expected_in_output",
    testdata_module_doc_not_exist,
)
class TestModuleDocNotExist(BaseClass):
    """Run the tests."""

    TEST_FOR_MODE = "interactive"
    UPDATE_FIXTURES = False
