""" tests for the utilities in utils
"""
from typing import List

import pytest

import ansible_navigator.utils as utils


@pytest.mark.parametrize(
    "value, anticpated_result",
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, [3]], [1, 2, 3]),
        ([1, [2], [3, 4], 5, True, {6: False}], [1, 2, 3, 4, 5, True, {6: False}]),
    ],
    ids=[
        "simple",
        "list with one list",
        "list detailed",
    ],
)
def test_flatten_list(value: List, anticpated_result: List) -> None:
    """test for flatten list"""
    actual_result = utils.flatten_list(value)
    assert list(actual_result) == anticpated_result
