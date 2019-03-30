from zmq_cache.zmq_server import Server
from zmq_cache.zmq_message import Message
from zmq_cache import zmq_message_types as mt


class CacheServer:

    _instances = {}

    def __init__(self, addr):
        if CacheServer._instances.get(addr) is not None:
            raise Exception('ZMQ cache server is a singleton, use CacheServer.get_instance(addr)')
        self.addr = addr
        self.cache = {}
        self.default = {}
        self.state = 'STOPPED'
        CacheServer._instances[addr] = self

    @staticmethod
    def get_instance(addr):
        inst = CacheServer._instances.get(addr)
        if inst is not None:
            return inst
        return CacheServer(addr)

    def set_table_default(self, table, default):
        self.default[table] = default

    def run(self):
        if self.state == 'RUNNING':
            raise Exception('ZMQ cache server at address {} is already running'.format(self.addr))
        self._reset_cache()
        server = Server(self.addr)
        self.state = 'RUNNING'
        try:
            while True:
                server.process(self._cache_operation)
        finally:
            server.close()
            self.state = 'STOPPED'

    def _reset_cache(self):
        self.cache.clear()
        for table, default in self.default.items():
            if callable(default):
                self.cache[table] = default()
            else:
                self.cache[table] = default

    def _cache_operation(self, msg):
        try:
            if msg.typ == mt.LIST_TABLE:
                return Message.make_rep_batch(list(self.cache))
            elif msg.typ == mt.RESET_CACHE:
                self._reset_cache()
                return Message.make_success(0)
            if not msg.table:
                return Message.make_error('table name cannot be empty in ZMQ cache request')
            table = self.cache.get(msg.table)
            if msg.typ == mt.GET:
                if table is None:
                    return Message.make_rep({})
                return Message.make_rep(table.get(msg.key, {}))
            elif msg.typ == mt.SET:
                if table is None:
                    table = {msg.key: msg.value}
                    self.cache[msg.table] = table
                else:
                    table[msg.key] = msg.value
                return Message.make_success(0)
            elif msg.typ == mt.DELETE:
                count = 0
                if table is not None:
                    if table.pop(msg.key, None) is not None:
                        count = 1
                    if not table:
                        self.cache.pop(msg.table, None)
                return Message.make_success(count)
            elif msg.typ == mt.QUERY:
                if table is None:
                    return Message.make_rep_batch({})
                return Message.make_rep_batch(table)
            elif msg.typ == mt.GET_BATCH:
                if table is None:
                    return Message.make_rep_batch({})
                return Message.make_rep_batch({key: table.get(key, None) for key in msg.keys})
            elif msg.typ == mt.SET_BATCH:
                if table is None:
                    self.cache[msg.table] = msg.entries
                else:
                    table.update(msg.entries)
                return Message.make_success(0)
            elif msg.typ == mt.DELETE_BATCH:
                if table is not None:
                    count = 0
                    for key in msg.keys:
                        if table.pop(key, None) is not None:
                            count += 1
                    if not table:
                        self.cache.pop(msg.table, None)
                    return Message.make_success(count)
                return Message.make_success(0)
            elif msg.typ == mt.DELETE_ALL:
                if table is not None:
                    size = len(table)
                    self.cache.pop(msg.table, None)
                    return Message.make_success(size)
                return Message.make_success(0)
            elif msg.typ == mt.RESET_TABLE:
                if table is not None:
                    self.cache.pop(msg.table, None)
                default = self.default.get(msg.table)
                if default:
                    if callable(default):
                        self.cache[msg.table] = default()
                    else:
                        self.cache[msg.table] = default
                return Message.make_success(0)
            elif msg.typ == mt.TABLE_SIZE:
                if table is None:
                    return Message.make_success(0)
                return Message.make_success(len(table))
            else:
                return Message.make_error('Message type {} is not supported on scheduler ZMQ server'.format(msg.typ))
        except Exception as e:
            return Message.make_error(str(e))
