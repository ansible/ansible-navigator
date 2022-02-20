"""Test KVS from share.ansible_navigator."""

import os
import sys
import types

import pytest

from ansible_navigator.utils.key_value_store import KeyValueStore


def test_kvs_save_restore(empty_kvs):
    """Test basic KVS write to disk and restore."""
    empty_kvs["hello"] = "whooop"
    empty_kvs["i_am_a_key"] = "and I am a value"
    empty_kvs.close()

    kvs2 = KeyValueStore(empty_kvs.path)
    assert kvs2["hello"] == "whooop"
    assert kvs2["i_am_a_key"] == "and I am a value"


def test_kvs_len(kvs):
    """Test KVS __len__ / len()"""
    assert len(kvs) == 4
    kvs["new_key"] = "something"
    assert len(kvs) == 5


def test_kvs_iterkeys(kvs):
    """Test KVS iterkeys()"""
    # Is it truly an iterator?
    assert isinstance(kvs.iterkeys(), types.GeneratorType)

    # Does it have all the keys we expect? (sorted because dicts don't care
    # about order)
    assert sorted(list(kvs.iterkeys())) == ["apple", "banana", "grape", "strawberry"]


def test_kvs_itervalues(kvs):
    """Test KVS itervalues()"""
    # Is it truly an iterator?
    assert isinstance(kvs.itervalues(), types.GeneratorType)

    # Does it have all the values we expect? (sorted because dicts don't care
    # about order)
    assert sorted(list(kvs.itervalues())) == ["green", "red", "red", "yellow"]


def test_kvs_iteritems(kvs):
    """Test KVS iteritems()"""
    # Is it truly an iterator?
    assert isinstance(kvs.iteritems(), types.GeneratorType)

    # Does it have all the items we expect? (sorted because dicts don't care
    # about order)
    assert sorted(list(kvs.iteritems())) == [
        ("apple", "red"),
        ("banana", "yellow"),
        ("grape", "green"),
        ("strawberry", "red"),
    ]


# Now things get weird.


def test_kvs_keys(kvs):
    """Test KVS keys()"""
    # We get back a KVSKeysView which is just a collections.abc.KeysView in
    # disguise.
    keys = kvs.keys()
    assert "banana" in keys
    assert "foo" not in keys
    assert len(keys) == len(kvs)
    assert sorted(list(keys)) == ["apple", "banana", "grape", "strawberry"]


def test_kvs_values(kvs):
    """Test KVS values()"""
    # We get back a KVSValuesView which is just a collections.abc.ValuesView in
    # disguise.
    values = kvs.values()
    assert "red" in values
    assert "blue" not in values
    assert len(values) == len(kvs)
    assert sorted(list(values)) == ["green", "red", "red", "yellow"]


def test_kvs_items(kvs):
    """Test KVS items()"""
    # We get back a KVSItemsView which is just a collections.abc.ItemsView in
    # disguise.
    items = kvs.items()
    assert ("banana", "yellow") in items
    assert ("banana", "blue") not in items
    assert len(items) == len(kvs)
    assert sorted(list(kvs.items())) == [
        ("apple", "red"),
        ("banana", "yellow"),
        ("grape", "green"),
        ("strawberry", "red"),
    ]


def test_kvs_repr(kvs, empty_kvs):
    """Test KVS __repr__()"""
    assert repr(kvs) == (
        "KeyValueStore([('apple', 'red'), ('banana', 'yellow'), "
        "('grape', 'green'), ('strawberry', 'red')])"
    )

    assert repr(empty_kvs) == "KeyValueStore()"
