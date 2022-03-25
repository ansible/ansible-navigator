"""Tests for utils.dict_merge."""
from collections import deque

import pytest

from ansible_navigator.utils.dict_merge import DictMergeError
from ansible_navigator.utils.dict_merge import in_place_list_replace


def test_in_place_list_replace_basic():
    """Test the in_place_list_replace function, basic case."""
    left = {"a": 1, "b": 2}
    right = {"b": 3, "c": 4}
    in_place_list_replace(left, right)
    assert left == {"a": 1, "b": 3, "c": 4}


def test_in_place_list_replace_list():
    """Test the in_place_list_replace function, list case."""
    left = {"a": 1, "b": [0, 1, 2]}
    right = {"b": ["a", "b", "c"], "c": 4}
    in_place_list_replace(left, right)
    assert left == {"a": 1, "b": ["a", "b", "c"], "c": 4}


def test_in_place_list_replace_nested():
    """Test the in_place_list_replace function, list case."""
    left = {"a": {"a": {"a": {"a": "left", "b": "left"}}}}
    right = {"a": {"a": {"a": {"a": "right"}}}}
    in_place_list_replace(left, right)
    assert left == {"a": {"a": {"a": {"a": "right", "b": "left"}}}}


def test_in_place_list_replace_primitive():
    """Test the in_place_list_replace function, primitive case."""
    left = {"a": True}
    right = {"a": "b"}
    in_place_list_replace(left, right)
    assert left == {"a": "b"}


def test_in_place_list_replace_right_not_dict():
    """Test the in_place_list_replace function, non-dict right."""
    left = {"a": {}}
    right = {"a": True}
    with pytest.raises(DictMergeError):
        in_place_list_replace(left, right)


def test_in_place_list_replace_left_off():
    """Test the in_place_list_replace function, non-dict right."""
    left = {"a": deque([1, 2, 3])}
    right = {"a": True}
    with pytest.raises(DictMergeError):
        in_place_list_replace(left, right)
