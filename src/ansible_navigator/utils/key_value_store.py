"""An interface to use a sqlite database as a key-value store."""
from __future__ import annotations

import sqlite3

from collections.abc import ItemsView
from collections.abc import Iterator
from collections.abc import KeysView
from collections.abc import MutableMapping
from collections.abc import ValuesView
from pathlib import Path


class KVSKeysView(KeysView[str]):
    """A glorified KeysView specific to, and returned by, methods in KeyValueStore."""


class KVSItemsView(ItemsView[str, str]):
    """A glorified ItemsView specific to, and returned by, methods in KeyValueStore."""


class KVSValuesView(ValuesView[str]):
    """A glorified ValuesView specific to, and returned by, methods in KeyValueStore."""


class KeyValueStore(MutableMapping[str, str]):
    """An interface to use a sqlite database as a key-value store."""

    def __init__(self, filename: str | Path):
        """Initialize the key-value store.

        :param filename: The full path to the sqlite database file
        """
        self._path = str(filename)
        self.conn = sqlite3.connect(self._path)
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS kv (key text unique, value text)")

    @property
    def path(self) -> str:
        """Provide the filename where the KVS is stored on disk.

        :returns: The path to the key-value store
        """
        return self._path

    def close(self) -> None:
        """Close the connection to the database."""
        self.conn.commit()
        self.conn.close()

    def open_(self) -> sqlite3.Connection:
        """Establish the connection to the database.

        :returns: A connection to the database
        """
        self.conn = sqlite3.connect(self.path)
        return self.conn

    def __len__(self) -> int:
        """Count the number of keys in the key-value store.

        :returns: The number of keys
        """
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT COUNT(*) FROM kv").fetchone()[0]
        return rows if rows is not None else 0

    def iterkeys(self) -> Iterator[str]:
        """Yield keys from the key-value store one by one.

        :yields: The keys in the key-value store
        """
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT key FROM kv"):
            yield row[0]

    def itervalues(self) -> Iterator[str]:
        """Yield values from the key-value store one by one.

        :yields: The values in the key-value store
        """
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT value FROM kv"):
            yield row[0]

    def iteritems(self) -> Iterator[tuple[str, str]]:
        """Yield items from the key-value store one by one.

        :yields: The key-value store as items (key, value)
        """
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT key, value FROM kv"):
            yield row[0], row[1]

    def keys(self) -> KVSKeysView:
        """Return all keys in the key-value store.

        :returns: All the keys
        """
        return KVSKeysView(self)

    def values(self) -> KVSValuesView:
        """Return all values in the key-value store.

        :returns: All the values
        """
        return KVSValuesView(self)

    def items(self) -> KVSItemsView:
        """Return all items from the key-value store.

        :returns: The key-value store as items (key, value)
        """
        return KVSItemsView(self)

    # mypy complains about this 'str' because it's more specific than the 'object'
    # that dict's Mapping superclass wants. However, it's correct in our case.
    # Our sqlite table expects string keys (column type 'text'). It's an error to
    # pass something else. If we pass something too weird, the sqlite3 lib will
    # throw an error at runtime.
    def __contains__(self, key: str) -> bool:  # type: ignore[override]
        """Check if a given key is in the key-value store.

        This provides dictionary like  `some_key in` support for the key-value store.

        :param key: The key to search for
        :returns: An indication of the provided key's existence in the key-value store
        """
        cursor = self.conn.cursor()
        return cursor.execute("SELECT 1 FROM kv WHERE key = ?", (key,)).fetchone() is not None

    def __getitem__(self, key: str) -> str:
        """Return a value from the key-value store given a key.

        :param key: The key to find
        :raises KeyError: When the key does not exist in the key-value store
        :returns: The value for the key provided
        """
        cursor = self.conn.cursor()
        item = cursor.execute("SELECT value FROM kv WHERE key = ?", (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key: str, value: str) -> None:
        """Place a key-value combination in the key-value store.

        :param key: The key of the combination to set
        :param value: The value of the combination to set
        """
        cursor = self.conn.cursor()
        cursor.execute("REPLACE INTO kv (key, value) VALUES (?,?)", (key, value))

    def __delitem__(self, key: str) -> None:
        """Delete a key-value combination in the key-value store.

        :param key: The key of the entry to delete
        :raises KeyError: When the provided key does not exist in the key-value store
        """
        if key not in self:
            raise KeyError(key)
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM kv WHERE key = ?", (key,))

    def __iter__(self) -> Iterator[str]:
        """Yield values extracted from the key-value store one by one.

        This provides dictionary like `for key in` support for the key-value store.

        :returns: The keys in the key-value store
        """
        return self.iterkeys()

    def __repr__(self) -> str:
        """Represent the key-value store.

        :returns: Representation of the key-value store
        """
        # Loosely based on collections.OrderedDict#__repr__
        if not self:
            return f"{self.__class__.__name__}()"
        return f"{self.__class__.__name__}({list(self.items())})"
