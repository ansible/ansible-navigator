"""Test KVS from ansible_navigator.utils."""

import types

from ansible_navigator.utils.key_value_store import KeyValueStore


def test_kvs_save_restore(empty_kvs: KeyValueStore):
    """Test basic KVS write to disk and restore.

    :param empty_kvs: An empty key-value store
    """
    empty_kvs["hello"] = "whoop"
    empty_kvs["i_am_a_key"] = "and I am a value"
    empty_kvs.close()

    kvs2 = KeyValueStore(empty_kvs.path)
    assert kvs2["hello"] == "whoop"
    assert kvs2["i_am_a_key"] == "and I am a value"


def test_kvs_len(kvs: KeyValueStore):
    """Test KVS __len__ / len().

    :param kvs: A key-value store populated with data
    """
    assert len(kvs) == 4
    kvs["new_key"] = "something"
    assert len(kvs) == 5


def test_kvs_iterkeys(kvs: KeyValueStore):
    """Test KVS iterkeys().

    :param kvs: A key-value store populated with data
    """
    # Is it truly an iterator?
    assert isinstance(kvs.iterkeys(), types.GeneratorType)

    # Does it have all the keys we expect? (sorted because dicts don't care
    # about order)
    assert sorted(list(kvs.iterkeys())) == ["apple", "banana", "grape", "strawberry"]


def test_kvs_itervalues(kvs: KeyValueStore):
    """Test KVS itervalues().

    :param kvs: A key-value store populated with data
    """
    # Is it truly an iterator?
    assert isinstance(kvs.itervalues(), types.GeneratorType)

    # Does it have all the values we expect? (sorted because dicts don't care
    # about order)
    assert sorted(list(kvs.itervalues())) == ["green", "red", "red", "yellow"]


def test_kvs_iteritems(kvs: KeyValueStore):
    """Test KVS iteritems().

    :param kvs: A key-value store populated with data
    """
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


def test_kvs_keys(kvs: KeyValueStore):
    """Test KVS keys().

    :param kvs: A key-value store populated with data
    """
    # We get back a KVSKeysView which is just a collections.abc.KeysView in
    # disguise.
    keys = kvs.keys()
    assert "banana" in keys
    assert "foo" not in keys
    assert len(keys) == len(kvs)
    assert sorted(list(keys)) == ["apple", "banana", "grape", "strawberry"]


def test_kvs_values(kvs: KeyValueStore):
    """Test KVS values().

    :param kvs: A key-value store populated with data
    """
    # We get back a KVSValuesView which is just a collections.abc.ValuesView in
    # disguise.
    values = kvs.values()
    assert "red" in values
    assert "blue" not in values
    assert len(values) == len(kvs)
    assert sorted(list(values)) == ["green", "red", "red", "yellow"]


def test_kvs_items(kvs: KeyValueStore):
    """Test KVS items().

    :param kvs: A key-value store populated with data
    """
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


def test_kvs_repr(kvs: KeyValueStore, empty_kvs: KeyValueStore):
    """Test KVS __repr__().

    :param empty_kvs: An empty key-value store
    :param kvs: A key-value store populated with data
    """
    assert repr(kvs) == (
        "KeyValueStore([('apple', 'red'), ('banana', 'yellow'), "
        "('grape', 'green'), ('strawberry', 'red')])"
    )

    assert repr(empty_kvs) == "KeyValueStore()"
