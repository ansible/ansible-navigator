"""Tests for the key value store module."""
# pylint: disable=redefined-outer-name

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ansible_navigator.utils.key_value_store import KeyValueStore


if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def kvs(tmp_path: Path) -> KeyValueStore:
    """Provide a fresh KeyValueStore instance.

    Args:
        tmp_path: Temporary directory

    Returns:
        A KeyValueStore instance
    """
    return KeyValueStore(tmp_path / "test.db")


def test_path_property(kvs: KeyValueStore) -> None:
    """Test path property returns the database path."""
    assert kvs.path.endswith("test.db")


def test_set_and_get(kvs: KeyValueStore) -> None:
    """Test setting and getting a value."""
    kvs["key1"] = "value1"
    assert kvs["key1"] == "value1"


def test_get_missing_key(kvs: KeyValueStore) -> None:
    """Test getting a missing key raises KeyError."""
    with pytest.raises(KeyError):
        kvs["missing"]


def test_overwrite_value(kvs: KeyValueStore) -> None:
    """Test overwriting an existing key."""
    kvs["key"] = "old"
    kvs["key"] = "new"
    assert kvs["key"] == "new"


def test_delete_key(kvs: KeyValueStore) -> None:
    """Test deleting a key."""
    kvs["key"] = "value"
    del kvs["key"]
    assert "key" not in kvs


def test_delete_missing_key(kvs: KeyValueStore) -> None:
    """Test deleting a missing key raises KeyError."""
    with pytest.raises(KeyError):
        del kvs["missing"]


def test_contains(kvs: KeyValueStore) -> None:
    """Test the in operator."""
    kvs["key"] = "value"
    assert "key" in kvs
    assert "missing" not in kvs


def test_len_empty(kvs: KeyValueStore) -> None:
    """Test len on empty store."""
    assert len(kvs) == 0


def test_len_with_items(kvs: KeyValueStore) -> None:
    """Test len with items."""
    kvs["a"] = "1"
    kvs["b"] = "2"
    assert len(kvs) == 2


def test_iterkeys(kvs: KeyValueStore) -> None:
    """Test iterkeys yields all keys."""
    kvs["a"] = "1"
    kvs["b"] = "2"
    assert sorted(kvs.iterkeys()) == ["a", "b"]


def test_itervalues(kvs: KeyValueStore) -> None:
    """Test itervalues yields all values."""
    kvs["a"] = "1"
    kvs["b"] = "2"
    assert sorted(kvs.itervalues()) == ["1", "2"]


def test_iteritems(kvs: KeyValueStore) -> None:
    """Test iteritems yields all items."""
    kvs["a"] = "1"
    kvs["b"] = "2"
    items = sorted(kvs.iteritems())
    assert items == [("a", "1"), ("b", "2")]


def test_keys_view(kvs: KeyValueStore) -> None:
    """Test keys returns a view."""
    kvs["a"] = "1"
    kvs["b"] = "2"
    keys = kvs.keys()
    assert "a" in keys
    assert "b" in keys


def test_values_view(kvs: KeyValueStore) -> None:
    """Test values returns a view."""
    kvs["a"] = "1"
    values = kvs.values()
    assert "1" in values


def test_items_view(kvs: KeyValueStore) -> None:
    """Test items returns a view."""
    kvs["a"] = "1"
    items = kvs.items()
    assert ("a", "1") in items


def test_iter(kvs: KeyValueStore) -> None:
    """Test iterating over the store yields keys."""
    kvs["a"] = "1"
    kvs["b"] = "2"
    assert sorted(kvs) == ["a", "b"]


def test_repr_empty(kvs: KeyValueStore) -> None:
    """Test repr of empty store."""
    assert repr(kvs) == "KeyValueStore()"


def test_repr_with_items(kvs: KeyValueStore) -> None:
    """Test repr of store with items."""
    kvs["key"] = "val"
    result = repr(kvs)
    assert "KeyValueStore" in result
    assert "key" in result
    assert "val" in result


def test_close_and_reopen(tmp_path: Path) -> None:
    """Test closing and reopening the store preserves data."""
    db_path = tmp_path / "persist.db"
    kvs = KeyValueStore(db_path)
    kvs["key"] = "value"
    kvs.close()

    kvs2 = KeyValueStore(db_path)
    assert kvs2["key"] == "value"
    kvs2.close()


def test_open_method(kvs: KeyValueStore) -> None:
    """Test open_ method returns a connection."""
    conn = kvs.open_()
    assert conn is not None


def test_init_with_path_object(tmp_path: Path) -> None:
    """Test initialization with a Path object."""
    kvs = KeyValueStore(tmp_path / "pathobj.db")
    kvs["test"] = "value"
    assert kvs["test"] == "value"
