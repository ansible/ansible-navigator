"""Fixtures for share tests."""

from collections.abc import Generator
from pathlib import Path

import pytest

from ansible_navigator.utils.key_value_store import KeyValueStore


@pytest.fixture
def empty_kvs(tmp_path: Path) -> Generator[KeyValueStore, None, None]:
    """Give us a temporary, empty KeyValueStore.

    Args:
        tmp_path: Path to a temporary directory

    Yields:
        The temporary KVS
    """
    database_path = tmp_path / "basic_kvs_usage.db"
    yield KeyValueStore(database_path)


@pytest.fixture
def kvs(tmp_path: Path) -> Generator[KeyValueStore, None, None]:
    """Give us a temporary KeyValueStore with some data.

    Args:
        tmp_path: Path to a temporary directory

    Yields:
        The temporary KVS
    """
    database_path = tmp_path / "basic_kvs_usage.db"
    key_value_store = KeyValueStore(database_path)
    key_value_store["banana"] = "blue"  # yuck
    key_value_store["apple"] = "red"
    key_value_store["grape"] = "green"
    key_value_store["strawberry"] = "red"
    key_value_store["banana"] = "yellow"  # just kidding
    key_value_store["cherry"] = "red"
    del key_value_store["cherry"]
    yield key_value_store
