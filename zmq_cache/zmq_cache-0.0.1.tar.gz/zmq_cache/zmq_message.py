import json
from collections import namedtuple

from zmq_cache import zmq_message_types as mt


class Message:

    def __init__(self,
                 typ,
                 table=None,
                 message=None,
                 key=None,
                 value=None,
                 query=None,
                 keys=None,
                 entries=None,
                 count=None):
        self.typ = typ
        if table is not None:
            self.table = table
        if message is not None:
            self.message = message
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value
        if query is not None:
            self.query = query
        if keys is not None:
            self.keys = keys
        if entries is not None:
            self.entries = entries
        if count is not None:
            self.count = count

    @staticmethod
    def make_list_table():
        return Message(mt.LIST_TABLE)

    @staticmethod
    def make_reset_cache():
        return Message(mt.RESET_CACHE)

    @staticmethod
    def make_delete(table, key):
        return Message(mt.DELETE, table=table, key=key)

    @staticmethod
    def make_set(table, key, value):
        return Message(mt.SET, table=table, key=key, value=value)

    @staticmethod
    def make_get(table, key):
        return Message(mt.GET, table=table, key=key)

    @staticmethod
    def make_query(table, query_string):
        return Message(mt.QUERY, table=table, query=query_string)

    @staticmethod
    def make_delete_batch(table, keys):
        return Message(mt.DELETE_BATCH, table=table, keys=keys)

    @staticmethod
    def make_delete_all(table):
        return Message(mt.DELETE_ALL, table=table)

    @staticmethod
    def make_set_batch(table, entries):
        return Message(mt.SET_BATCH, table=table, entries=entries)

    @staticmethod
    def make_get_batch(table, keys):
        return Message(mt.GET_BATCH, table=table, keys=keys)

    @staticmethod
    def make_reset_table(table):
        return Message(mt.RESET_TABLE, table=table)

    @staticmethod
    def make_table_size(table):
        return Message(mt.TABLE_SIZE, table=table)

    @staticmethod
    def make_success(count):
        return Message(mt.SUCCESS, count=count)

    @staticmethod
    def make_error(error_msg):
        return Message(mt.ERROR, message=error_msg)

    @staticmethod
    def make_rep(value):
        return Message(mt.REP, value=value)

    @staticmethod
    def make_rep_batch(entries):
        return Message(mt.REP_BATCH, entries=entries)

    @staticmethod
    def from_bytes(binary):
        fields = json.loads(binary.decode('utf-8'))
        return namedtuple('Message', fields.keys())(*fields.values())

    def to_bytes(self):
        return json.dumps(vars(self)).encode('utf-8')
