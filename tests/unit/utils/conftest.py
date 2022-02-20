"""fixtures for share tests"""

import os
import sys

import pytest

from ansible_navigator.utils.key_value_store import KeyValueStore


@pytest.fixture
def empty_kvs(tmp_path):
    """
    Gives us a temporary, empty KeyValueStore.

    :returns: the temporary KVS
    """
    db = tmp_path / "basic_kvs_usage.db"
    yield KeyValueStore(db)


@pytest.fixture
def kvs(tmp_path):
    """
    Gives us a temporary KeyValueStore with some data.

    :returns: the temporary KVS
    """
    db = tmp_path / "basic_kvs_usage.db"
    kvs = KeyValueStore(db)
    kvs["banana"] = "blue"  # ewww
    kvs["apple"] = "red"
    kvs["grape"] = "green"
    kvs["strawberry"] = "red"
    kvs["banana"] = "yellow"  # just kidding
    kvs["cherry"] = "red"
    del kvs["cherry"]
    yield kvs
