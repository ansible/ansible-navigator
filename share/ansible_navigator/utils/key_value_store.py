"""An interface to use a sqlite database as a key-value store."""
import sqlite3


class KeyValueStore(dict):
    """An interface to use a sqlite database as a key-value store."""

    def __init__(self, filename):
        """Initialize the key-value store.

        :param filename: The full path to the sqlite database file
        """
        # pylint: disable=super-init-not-called
        self.conn = sqlite3.connect(filename)
        self.path = filename
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS kv (key text unique, value text)")

    def close(self):
        """Close the connections to the database."""
        self.conn.commit()
        self.conn.close()

    def open(self):
        """Establish the connection to the database."""
        self.conn = sqlite3.connect(self.path)

    def __len__(self):
        """Determine the number of keys in the key-value store.

        :returns: The number of keys
        """
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT COUNT(*) FROM kv").fetchone()[0]
        return rows if rows is not None else 0

    def iterkeys(self):
        """Iterate the keys in the key-value store.

        :yields: The keys in the key-value store
        """
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT key FROM kv"):
            yield row[0]

    def itervalues(self):
        """Iterate the values in the key-value store.

        :yields: The values in the key-value store
        """
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT value FROM kv"):
            yield row[0]

    def iteritems(self):
        """Iterate the entries in the key-value store.

        :yields: The key-value store as items (key, value)
        """
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT key, value FROM kv"):
            yield row[0], row[1]

    def keys(self):
        """Return all the keys in the key-value store.

        :returns: All the keys
        """
        return list(self.iterkeys())

    def values(self):
        """Return all the values in the key-value store.

        :returns: All the values
        """
        return list(self.itervalues())

    def items(self):
        """Return the entries from the key-value store.

        :returns: The key-value store as items (key, value)
        """
        return list(self.iteritems())

    def __contains__(self, key):
        """Determine if a given key is in the key-value store.

        This provides dictionary like  `some_key in` support for the key-value store.

        :param key: The key to search for
        :returns: An indication of the provided key's existence in the key-value store
        """
        cursor = self.conn.cursor()
        return cursor.execute("SELECT 1 FROM kv WHERE key = ?", (key,)).fetchone() is not None

    def __getitem__(self, key):
        """Retrieve a value from the key-value store given a key.

        :param key: The key to find
        :raises KeyError: When the key does not exist in the key-value store
        :returns: The value for the key provided
        """
        cursor = self.conn.cursor()
        item = cursor.execute("SELECT value FROM kv WHERE key = ?", (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):
        """Set a key-value combination in the key-value store.

        :param key: The key of the combination to set
        :param value: The value of the combination to set
        """
        cursor = self.conn.cursor()
        cursor.execute("REPLACE INTO kv (key, value) VALUES (?,?)", (key, value))

    def __delitem__(self, key):
        """Delete an key-value combination in the key-value store.

        :param key: The key of the entry to delete
        :raises KeyError: When the provided key does not exist in the key-value store
        """
        if key not in self:
            raise KeyError(key)
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM kv WHERE key = ?", (key,))

    def __iter__(self):
        """Iterate the entries in the key-value store.

        This provides dictionary like `for key in` support for the key-value store.

        :returns: The keys in the key-value store
        """
        return self.iterkeys()
