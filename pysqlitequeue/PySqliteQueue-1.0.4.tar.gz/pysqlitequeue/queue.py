import pickle
import sqlite3


class SqliteQueue:
    _QUERY_INIT_TABLE = 'CREATE TABLE queue (id integer primary key, item blob);'
    _QUERY_INSERT_ITEM = 'INSERT INTO queue (item) VALUES (?);'
    _QUERY_SELECT_LAST_ITEM = 'SELECT item FROM queue ORDER BY id ASC LIMIT 1;'
    _QUERY_REMOVE_LAST_ITEM = 'DELETE FROM queue WHERE id=(SELECT min(id) FROM queue)'
    _QUERY_COUNT = 'SELECT COUNT(*) FROM queue;'

    def __init__(self, *args, **kwargs):
        self._conn = sqlite3.connect(*args, **kwargs)

        self._conn.execute(self._QUERY_INIT_TABLE)
        self._conn.commit()

    def put(self, item):
        self._conn.execute(self._QUERY_INSERT_ITEM, (sqlite3.Binary(pickle.dumps(item)),))
        self._conn.commit()

        return self

    def peek(self):
        item = self._conn.execute(self._QUERY_SELECT_LAST_ITEM).fetchone()

        if item:
            return pickle.loads(item[0])
        else:
            return None

    def poll(self):
        item = self._conn.execute(self._QUERY_SELECT_LAST_ITEM).fetchone()

        if item:
            item = item[0]
            self._conn.execute(self._QUERY_REMOVE_LAST_ITEM)
            self._conn.commit()
            return pickle.loads(item)
        else:
            return None

    def size(self) -> int:
        item = self._conn.execute(self._QUERY_COUNT).fetchone()
        return item[0]

    def empty(self) -> bool:
        return self.size() == 0
