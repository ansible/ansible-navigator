"""Tests for dot path functions."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import MutableMapping

import pytest

from ansible_navigator.utils.dot_paths import MergeBehaviors
from ansible_navigator.utils.dot_paths import ascendants_from_path
from ansible_navigator.utils.dot_paths import check_path
from ansible_navigator.utils.dot_paths import delete_with_path
from ansible_navigator.utils.dot_paths import descendants_to_path
from ansible_navigator.utils.dot_paths import get_with_path
from ansible_navigator.utils.dot_paths import move_to_path
from ansible_navigator.utils.dot_paths import place_at_path
from ansible_navigator.utils.dot_paths import remove_and_delete_empty_ascendants


def test_ascendants_from_path():
    """Test ascendant from path."""
    path = "a.b.c.d.e"
    assert ascendants_from_path(path) == ["a.b.c.d.e", "a.b.c.d", "a.b.c", "a.b", "a"]


def test_check_path():
    """Test check path."""
    content = {"a": {"b": {"c": {"d": {"e": "f"}}}}}
    path = "a.b.c.d.e"
    assert check_path(content, path)
    path = "a.b.c.d.e.f"
    assert not check_path(content, path)


def test_delete_with_path():
    """Test delete with path."""
    content = {"a": {"b": {"c": {"d": {"e": "f"}}}}}
    path = "a.b.c.d.e"
    delete_with_path(content, path)
    assert content == {"a": {"b": {"c": {"d": {}}}}}


def test_descendants_to_path():
    """Test descendants to path."""
    path = "a.b.c.d.e"
    assert descendants_to_path(path) == ["a", "a.b", "a.b.c", "a.b.c.d", "a.b.c.d.e"]


def test_get_with_path():
    """Test get with path."""
    content = {"a": {"b": {"c": {"d": {"e": "f"}}}}}
    path = "a.b.c.d.e"
    assert get_with_path(content, path) == "f"


def test_remove_and_delete_empty_ascendants_changed():
    """Test remove and delete empty ascendants."""
    content = {"a": {"b": {"c": {"d": {"e": {}}}}}}
    path = "a.b.c.d.e"
    remove_and_delete_empty_ascendants(content, path)
    assert not content


def test_remove_and_delete_empty_ascendants_not_changed():
    """Test remove and delete empty ascendants."""
    content = {"a": {"b": {"c": {"d": {"e": {}, "ee": True}}}}}
    path = "a.b.c.d.ee"
    remove_and_delete_empty_ascendants(content, path)
    assert content == {"a": {"b": {"c": {"d": {"e": {}}}}}}


base_dict = {"root": {"dict": {"a": "b"}, "list": [1, 2, 3]}}


@dataclass
class Scenario:
    """Test data."""

    behaviors: tuple[MergeBehaviors, ...]
    comment: str
    path: str
    expected: MutableMapping | None
    value: bool | int | list | float | str | list | dict = ""
    content: dict = field(default_factory=lambda: base_dict)
    new_path: str = ""

    def __str__(self):
        """Provide string representation.

        :returns: String representation
        """
        return f"{self.comment}"


scenarios_place_success = (
    Scenario(
        behaviors=(MergeBehaviors.LIST_LIST_EXTEND,),
        comment="Test list list extend",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": [1, 2, 3, 4, 5, 6]}},
        value=[4, 5, 6],
    ),
    Scenario(
        behaviors=(MergeBehaviors.LIST_LIST_REPLACE,),
        comment="Test list list replace",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": [4, 5, 6]}},
        value=[4, 5, 6],
    ),
    Scenario(
        behaviors=(MergeBehaviors.LIST_APPEND,),
        comment="Test list append",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": [1, 2, 3, True]}},
        value=True,
    ),
    Scenario(
        behaviors=(MergeBehaviors.LIST_REPLACE,),
        comment="Test list replace",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": True}},
        value=True,
    ),
    Scenario(
        behaviors=(MergeBehaviors.LIST_REPLACE, MergeBehaviors.LIST_UNIQUE),
        comment="Test list replace, unique, not list",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": True}},
        value=True,
    ),
    Scenario(
        behaviors=(MergeBehaviors.LIST_LIST_EXTEND, MergeBehaviors.LIST_UNIQUE),
        comment="Test list list extend, unique",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": [1, 2, 3, 4, 5]}},
        value=[1, 4, 5],
    ),
    Scenario(
        behaviors=(MergeBehaviors.LIST_LIST_EXTEND, MergeBehaviors.LIST_SORT),
        comment="Test list list extend, sort",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": [0, 1, 1, 2, 3, 4]}},
        value=[1, 0, 4],
    ),
    Scenario(
        behaviors=(
            MergeBehaviors.LIST_LIST_EXTEND,
            MergeBehaviors.LIST_SORT,
            MergeBehaviors.LIST_UNIQUE,
        ),
        comment="Test list list extend, sort, unique",
        path="root.list",
        expected={"root": {"dict": {"a": "b"}, "list": [0, 1, 2, 3, 4]}},
        value=[1, 0, 4],
    ),
    Scenario(
        behaviors=(MergeBehaviors.DICT_DICT_UPDATE,),
        comment="Test dict dict update",
        path="root.dict",
        expected={"root": {"dict": {"a": "b", "c": "d"}, "list": [1, 2, 3]}},
        value={"c": "d"},
    ),
    Scenario(
        behaviors=(MergeBehaviors.DICT_DICT_REPLACE,),
        comment="Test dict dict replace",
        path="root.dict",
        expected={"root": {"dict": {"c": "d"}, "list": [1, 2, 3]}},
        value={"c": "d"},
    ),
    Scenario(
        behaviors=(MergeBehaviors.DICT_DICT_UPDATE,),
        comment="Test place at root",
        path="",
        expected={"bool": True, "root": {"dict": {"a": "b"}, "list": [1, 2, 3]}},
        value={"bool": True},
    ),
    Scenario(
        behaviors=(MergeBehaviors.DICT_DICT_REPLACE,),
        comment="Test mass replace",
        path="",
        expected={"bool": True},
        value={"bool": True},
    ),
    Scenario(
        behaviors=tuple(),
        comment="deep change str",
        content={"a": {"b": {"c": {"d": {"e": "f"}}}}},
        path="a.b.c.d.e",
        expected={"a": {"b": {"c": {"d": {"e": "g"}}}}},
        value="g",
    ),
    Scenario(
        behaviors=tuple(),
        comment="deep dict replace",
        content={"a": {"b": {"c": {"d": {"e": "f"}}}}},
        path="a.b.c.d",
        expected={"a": {"b": {"c": {"d": True}}}},
        value=True,
    ),
    Scenario(
        behaviors=tuple(),
        comment="deep dict placement",
        path="root.dict.aa.bb",
        expected={"root": {"dict": {"a": "b", "aa": {"bb": True}}, "list": [1, 2, 3]}},
        value=True,
    ),
)


@pytest.mark.parametrize("scenario", scenarios_place_success, ids=str)
def test_place_at_path_success(scenario: Scenario):
    """Test place at path.

    :param scenario: Test data.
    """
    updated = place_at_path(
        behaviors=scenario.behaviors,
        content=scenario.content,
        path=scenario.path,
        value=scenario.value,
    )
    assert updated == scenario.expected


scenarios_place_raise = (
    Scenario(
        behaviors=(MergeBehaviors.LIST_LIST_EXTEND, MergeBehaviors.LIST_LIST_REPLACE),
        comment="Test list list extend, list list replace",
        path="",
        expected=None,
        value="",
    ),
    Scenario(
        behaviors=(MergeBehaviors.DICT_DICT_REPLACE, MergeBehaviors.DICT_DICT_UPDATE),
        comment="Test dict dict replace, dict dict update",
        path="",
        expected=None,
        value="",
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test dict_dict",
        path="root.dict",
        expected=None,
        value={"c": "d"},
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test list_list behavior",
        path="root.list",
        expected=None,
        value=[4, 5, 6],
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test list behavior",
        path="root.list",
        expected=None,
        value=True,
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test mass replace",
        path="",
        expected=None,
        value={"bool": True},
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test mass replace",
        path="",
        expected=None,
        value=True,
    ),
)


@pytest.mark.parametrize("scenario", scenarios_place_raise, ids=str)
def test_place_at_path_raises(scenario: Scenario):
    """Test place at path.

    :param scenario: Test data.
    """
    with pytest.raises(ValueError):
        place_at_path(
            behaviors=scenario.behaviors,
            content=scenario.content,
            path=scenario.path,
            value=scenario.value,
        )


scenarios_move = (
    Scenario(
        behaviors=tuple(),
        comment="Test list move",
        path="root.list",
        new_path="root.list_moved",
        expected={"root": {"dict": {"a": "b"}, "list_moved": [1, 2, 3]}},
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test dict move",
        path="root.dict",
        new_path="root.dict_moved",
        expected={"root": {"dict_moved": {"a": "b"}, "list": [1, 2, 3]}},
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test dict move and cleanup",
        path="root.dict.a",
        new_path="root.dict.aa",
        expected={"root": {"dict": {"aa": "b"}, "list": [1, 2, 3]}},
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test move root nested",
        path="root",
        new_path="r0.r1.r2.r3",
        expected={"r0": {"r1": {"r2": {"r3": {"dict": {"a": "b"}, "list": [1, 2, 3]}}}}},
    ),
    Scenario(
        behaviors=tuple(),
        comment="Test move same ",
        path="root.dict",
        new_path="root.dict",
        expected={"root": {"dict": {"a": "b"}, "list": [1, 2, 3]}},
    ),
)


@pytest.mark.parametrize("scenario", scenarios_move, ids=str)
def test_move(scenario: Scenario):
    """Test move to path.

    :param scenario: Test data.
    """
    updated = move_to_path(
        behaviors=scenario.behaviors,
        content=scenario.content,
        old_path=scenario.path,
        new_path=scenario.new_path,
    )
    assert updated == scenario.expected
