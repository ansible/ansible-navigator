""" use sqlite as a k,v store
"""
import sqlite3


class KeyValueStore(dict):
    """use sqlite as a k,v store"""

    def __init__(self, filename):
        # pylint: disable=super-init-not-called
        self.conn = sqlite3.connect(filename)
        self.path = filename
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS kv (key text unique, value text)")

    def close(self):
        """close the connections"""
        self.conn.commit()
        self.conn.close()

    def open(self):
        """establish the connection"""
        self.conn = sqlite3.connect(self.path)

    def __len__(self):
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT COUNT(*) FROM kv").fetchone()[0]
        return rows if rows is not None else 0

    def iterkeys(self):
        """iterate keys"""
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT key FROM kv"):
            yield row[0]

    def itervalues(self):
        """iterate values"""
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT value FROM kv"):
            yield row[0]

    def iteritems(self):
        """iterate items"""
        cursor = self.conn.cursor()
        for row in cursor.execute("SELECT key, value FROM kv"):
            yield row[0], row[1]

    def keys(self):
        """return keys"""
        return list(self.iterkeys())

    def values(self):
        """return values"""
        return list(self.itervalues())

    def items(self):
        """return items"""
        return list(self.iteritems())

    def __contains__(self, key):
        """in"""
        cursor = self.conn.cursor()
        return cursor.execute("SELECT 1 FROM kv WHERE key = ?", (key,)).fetchone() is not None

    def __getitem__(self, key):
        """get"""
        cursor = self.conn.cursor()
        item = cursor.execute("SELECT value FROM kv WHERE key = ?", (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):
        """set"""
        cursor = self.conn.cursor()
        cursor.execute("REPLACE INTO kv (key, value) VALUES (?,?)", (key, value))

    def __delitem__(self, key):
        """del"""
        if key not in self:
            raise KeyError(key)
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM kv WHERE key = ?", (key,))

    def __iter__(self):
        """for"""
        return self.iterkeys()
