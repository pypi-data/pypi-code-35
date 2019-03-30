from zmq_cache_client.zmq_client import Client
from zmq_cache_client.zmq_message import Message
from zmq_cache_client import zmq_message_types as mt


class Cache:
    def __init__(self, addr):
        self.addr = addr
        self.client = Client.get_instance(addr)

    def table(self, name):
        return Table(self.addr, name)

    def list_table(self):
        msg = Message.make_list_table()
        rep = self.client.send_req(msg)
        if rep.typ == mt.REP_BATCH:
            return rep.entries
        error_handle(rep)

    def reset_cache(self, confirm=False):
        if not confirm:
            raise Exception('This operation reset all the cache tables, set confirm to True to proceed')
        msg = Message.make_reset_cache()
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return
        error_handle(rep)


class Table(Cache):
    def __init__(self, addr, name):
        super().__init__(addr)
        self.name = name

    def set(self, key, value):
        msg = Message.make_set(self.name, key, value)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return
        error_handle(rep)

    def get(self, key, default=None):
        msg = Message.make_get(self.name, key)
        rep = self.client.send_req(msg)
        if rep.typ == mt.REP:
            if not rep.value:
                return default
            return rep.value
        error_handle(rep)

    def delete(self, key):
        msg = Message.make_delete(self.name, key)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return rep.count
        error_handle(rep)

    def set_batch(self, entries):
        msg = Message.make_set_batch(self.name, entries)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return
        error_handle(rep)

    def get_batch(self, keys):
        msg = Message.make_get_batch(self.name, keys)
        rep = self.client.send_req(msg)
        if rep.typ == mt.REP_BATCH:
            return rep.entries
        error_handle(rep)

    def delete_batch(self, keys):
        msg = Message.make_delete_batch(self.name, keys)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return rep.count
        error_handle(rep)

    def delete_all(self):
        msg = Message.make_delete_all(self.name)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return rep.count
        error_handle(rep)

    def query(self):
        msg = Message.make_query(self.name, None)
        rep = self.client.send_req(msg)
        if rep.typ == mt.REP_BATCH:
            return rep.entries
        error_handle(rep)

    def reset(self):
        msg = Message.make_reset_table(self.name)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return
        error_handle(rep)

    def size(self):
        msg = Message.make_table_size(self.name)
        rep = self.client.send_req(msg)
        if rep.typ == mt.SUCCESS:
            return rep.count
        error_handle(rep)

def error_handle(rep):
    if rep.typ == mt.ERROR:
        raise Exception(rep.message)
    else:
        raise Exception('Invalid return message type {} received'.format(rep.typ))
