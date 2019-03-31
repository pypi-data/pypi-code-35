#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import os
import socket
#import select

from datetime import datetime
import thread

log = logging.getLogger('durus')

__all__ = ['Server']

#try:
#    #python3
#    import asyncio
#    Scheduler = asyncio.Task
#except ImportError:
#    import trollius as asyncio
#    import trollius.tasks as Scheduler

from durus.error import ConflictError, ReadConflictError
from durus.logger import is_logging
from durus.file_storage import FileStorage
from durus.serialize import extract_class_name, split_oids

from durus.storage_server import (
    DEFAULT_GCBYTES,
    STATUS_OKAY, STATUS_KEYERROR, STATUS_INVALID,
    ClientError,
    )
from durus.utils import (
    int4_to_str, int8_to_str, str_to_int4, str_to_int8,
    join_bytes,
    )

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 22972
PROTOCOL = int4_to_str(20001)
EXTENSION = '.durus'

# max_queued_connections_limit: Increase the maximum amount of queued connections 
# min: 16
# recommended: 128
max_queued_connections_limit = 32

__all__ = ['ConnectedClient', 'Server']

def database_names(path):
    """Return a list of all Durus database names in a given path."""
    for filename in os.listdir(path):
        name, ext = os.path.splitext(filename)
        if ext == EXTENSION:
            yield name


class ConnectedClient(object):

    def __init__(self, client_socket):
        f = self.f = client_socket.makefile()
        self.invalid = {}
        self.unused_oids = {}
        self._read = f.read
        self.write = f.write
        self.flush = f.flush
        self.close = f.close
        self.recv = client_socket.recv

    #@asyncio.coroutine
    def read(self, sizeof):
        # XXX prefer recv() over read() for connected sockets.
        return self.recv(int(sizeof))

    @property
    def closed(self):
        return self.f.closed


class Server(object):
    """Provides access to databases for xdserver clients.

    In most cases your code will not use this class directly.  Use
    :program:`xdserver` instead; see :doc:`server`.
    """

    handlers = {
        'A': 'handle_enumerate_all',
        'E': 'handle_enumerate_open',
        'Q': 'handle_quit',
        'V': 'handle_version',
        '.': 'handle_disconnect',
    }

    db_handlers = {
        'B': 'handle_bulk_read',
        'C': 'handle_commit',
        'D': 'handle_destroy',
        'L': 'handle_load',
        'M': 'handle_new_oids',
        'N': 'handle_new_oid',
        'O': 'handle_open',
        'P': 'handle_pack',
        'S': 'handle_sync',
        'X': 'handle_close',
    }

    def __init__(self, path, storage_class=FileStorage, host=DEFAULT_HOST, 
        port=DEFAULT_PORT):
        self.path = os.path.abspath(path)
        self.storage_class = storage_class
        self.host = host
        self.port = port
        # Database name -> open storage mapping.  By default all are closed.
        self.clients = set()
        self.storages = {}

    #@asyncio.coroutine
    def dispatch(self):
        conn = socket.socket() #server socket
        address = (self.host, self.port)
        # allow socket reuse to avoid TIME_WAIT connections
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # expunge socket before reconnecting
        fp = conn.makefile()
        fp.flush()
        conn.bind(address)
        conn.listen(max_queued_connections_limit)
        #conn.setblocking(False)
        log.debug('Listening on %s:%i' % address)
        while 1:
            client_socket, client_address = conn.accept()
            log.debug('Connection from %s:%s' % client_address)
            thread.start_new_thread(self.serve_to_client, 
                (client_socket,))

    #@asyncio.coroutine
    def serve_to_client(self, client_socket):
        """Serves a payload to a connected client"""
        while 1:
            client = ConnectedClient(client_socket)
            # Initialize per-storage state for the new client.
            client.invalid = dict(
                (db_name, set()) for db_name in self.storages)
            client.unused_oids = dict(
                (db_name, set()) for db_name in self.storages)
            self.clients.add(client)
            while not client.closed:
                try:
                    #command = client.read(1)
                    command = client.recv(1)
                except socket.error:
                    break
                else:
                    if command in self.handlers:
                        handler_name = self.handlers[command]
                        handler = getattr(self, handler_name)
                        handler(client)
                    elif command in self.db_handlers:
                        handler_name = self.db_handlers[command]
                        handler = getattr(self, handler_name)
                        # Get database name.
                        name_length = str_to_int4(client.recv(4))
                        db_name = client.recv(name_length)
                        handler(client, db_name)
                    client.flush()
        log.debug('Connection closed.')
        self.clients.remove(client)

    #
    # Server handlers.
    # 

    #@asyncio.coroutine
    def handle_enumerate_all(self, client):
        # A
        log.debug('Enumerate all')
        names = list(database_names(self.path))
        self._handle_enumerate_database_names(client, names)

    #@asyncio.coroutine
    def handle_enumerate_open(self, client):
        # E
        log.debug('Enumerate open')
        names = list(self.storages.keys())
        self._handle_enumerate_database_names(client, names)

    #@asyncio.coroutine
    def _handle_enumerate_database_names(self, client, names):
        client.write(int4_to_str(len(names)))
        for name in names:
            client.write(int4_to_str(len(name)))
            client.write(name)

    #@asyncio.coroutine
    def handle_quit(self, client):
        # Q
        log.debug('Quit')
        for storage in list(self.storages.values()):
            if storage is not None:
                storage.close()
        #thread.stop()
    #@asyncio.coroutine
    def handle_version(self, client):
        # V
        log.debug('Version')
        client.write(PROTOCOL)

    #@asyncio.coroutine
    def handle_disconnect(self, client):
        # D
        log.debug('Disconnect')
        client.close()

    #
    # Database handlers.
    #
    def _db_path(self, db_name):
        db_path = os.path.join(self.path, db_name + EXTENSION)
        db_path = os.path.abspath(db_path)
        if not db_path.startswith(self.path):
            raise RuntimeError('Malformed db name %s' % db_name)
        return db_path

    def _handle_invalidations(self, db_name, oids):
        for c in self.clients:
            c.invalid[db_name].update(oids)

    def _new_oids(self, client, db_name, storage, count):
        oids = []
        while len(oids) < count:
            oid = storage.new_oid()
            for c in self.clients:
                if oid in c.invalid[db_name]:
                    oid = None
                    break
            if oid is not None:
                oids.append(oid)
        client.unused_oids[db_name].update(oids)
        return oids

    def _report_load_record(self, storage):
        if storage.d_load_record and is_logging(5):
            log.debug('\n'.join('%8s: %s' % (value, key)
                             for key, value
                             in sorted(storage.d_load_record.items())))
            storage.d_load_record.clear()

    #@asyncio.coroutine
    def _send_load_response(self, client, db_name, storage, oid):
        if oid in client.invalid[db_name]:
            client.write(STATUS_INVALID)
        else:
            try:
                record = storage.load(oid)
            except KeyError:
                log.debug('KeyError %s', str_to_int8(oid))
                client.write(STATUS_KEYERROR)
            except ReadConflictError:
                log.debug('ReadConflictError %s', str_to_int8(oid))
                client.write(STATUS_INVALID)
            else:
                if is_logging(5):
                    class_name = extract_class_name(record)
                    if class_name in storage.d_load_record:
                        storage.d_load_record[class_name] += 1
                    else:
                        storage.d_load_record[class_name] = 1
                    log.debug('Load %-7s %s', str_to_int8(oid), class_name)
                client.write(STATUS_OKAY)
                client.write(int4_to_str(len(record)))
                client.write(record)

    def _sync_storage(self, db_name, storage):
        self._handle_invalidations(db_name, storage.sync())

    #@asyncio.coroutine
    def handle_bulk_read(self, client, db_name):
        # B
        log.debug('Bulk read %s' % db_name)
        storage = self.storages[db_name]
        number_of_oids = str_to_int4(client.read(4))
        oid_str_len = 8 * number_of_oids
        oid_str = client.read(oid_str_len)
        oids = split_oids(oid_str)
        for oid in oids:
            self._send_load_response(client, db_name, storage, oid)

    #@asyncio.coroutine
    def handle_commit(self, client, db_name):
        # C
        log.debug('Commit %s' % db_name)
        storage = self.storages[db_name]
        self._sync_storage(db_name, storage)
        invalid = client.invalid[db_name]
        client.write(int4_to_str(len(invalid)))
        client.write(join_bytes(invalid))
        client.flush()
        invalid.clear()
        tdata_len = str_to_int4(client.read(4))
        if tdata_len == 0:
            # Client decided not to commit (e.g. conflict)
            return
        tdata = client.read(tdata_len)
        logging_debug = is_logging(10)
        logging_debug and log.debug('Committing %s bytes', tdata_len)
        storage.begin()
        i = 0
        oids = []
        while i < tdata_len:
            rlen = str_to_int4(tdata[i:i+4])
            i += 4
            oid = tdata[i:i+8]
            record = tdata[i+8:i+rlen]
            i += rlen
            if logging_debug:
                class_name = extract_class_name(record)
                log.debug('  oid=%-6s rlen=%-6s %s',
                    str_to_int8(oid), rlen, class_name)
            storage.store(oid, record)
            oids.append(oid)
        assert i == tdata_len
        oid_set = set(oids)
        for c in self.clients:
            if c is not client:
                if oid_set.intersection(c.unused_oids[db_name]):
                    raise ClientError('invalid oid: %r' % oid)
        try:
            handle_invalidations = (
                lambda oids: self._handle_invalidations(db_name, oids))
            storage.end(handle_invalidations=handle_invalidations)
        except ConflictError:
            log.debug('Conflict during commit')
            client.write(STATUS_INVALID)
        else:
            self._report_load_record(storage)
            log.debug('Committed %3s objects %s bytes at %s',
                len(oids), tdata_len, datetime.now())
            client.write(STATUS_OKAY)
            client.unused_oids[db_name] -= oid_set
            for c in self.clients:
                if c is not client:
                    c.invalid[db_name].update(oids)
            storage.d_bytes_since_pack += tdata_len + 8

    #@asyncio.coroutine
    def handle_destroy(self, client, db_name):
        # D
        log.debug('Destroy %s' % db_name)
        if db_name in self.storages:
            # Do nothing if it's still in use.
            pass
        else:
            db_path = self._db_path(db_name)
            os.unlink(db_path)

    #@asyncio.coroutine
    def handle_load(self, client, db_name):
        # L
        log.debug('Load %s' % db_name)
        log.debug('Client %r' % client)
        if not db_name in self.storages:
            log.debug("Database not open yet?")
            self.handle_open(client, db_name)
        storage = self.storages[db_name]
        oid = client.read(8)
        self._send_load_response(client, db_name, storage, oid)

    #@asyncio.coroutine
    def handle_new_oids(self, client, db_name):
        # M
        log.debug('New OIDs %s' % db_name)
        storage = self.storages[db_name]
        count = ord(client.read(1))
        log.debug('oids: %s', count)
        client.write(
            join_bytes(self._new_oids(client, db_name, storage, count)))

    #@asyncio.coroutine
    def handle_new_oid(self, client, db_name):
        # N
        log.debug( 'New OID %s' % db_name)
        storage = self.storages[db_name]
        client.write(self._new_oids(client, db_name, storage, 1)[0])

    #@asyncio.coroutine
    def handle_open(self, client, db_name):
        # O
        log.debug( 'Open %s' % db_name)
        if db_name not in self.storages:
            db_path = self._db_path(db_name)
            storage = self.storage_class(db_path)
            storage.d_bytes_since_pack = 0
            storage.d_load_record = {}
            storage.d_packer = None
            self.storages[db_name] = storage
            # Initialize per-storage state for each client.
            for c in self.clients:
                c.invalid[db_name] = set()
                c.unused_oids[db_name] = set()

    #@asyncio.coroutine
    def handle_pack(self, client, db_name):
        # P
        log.debug( 'Pack %s' % db_name)
        storage = self.storages[db_name]
        if storage.d_packer is None:
            log.debug( 'Pack started at %s' % datetime.now())
            storage.d_packer = storage.get_packer()
            if storage.d_packer is None:
                log.debug( 'Cannot iteratively pack, performing full pack.')
                storage.pack()
                log.debug( 'Pack completed at %s' % datetime.now())
        else:
            log.debug( 'Pack already in progress at %s' % datetime.now())
        client.write(STATUS_OKAY)

    #@asyncio.coroutine
    def handle_sync(self, client, db_name):
        # S
        log.debug('Sync %s' % db_name)
        storage = self.storages[db_name]
        self._report_load_record(storage)
        self._sync_storage(db_name, storage)
        invalid = client.invalid[db_name]
        log.debug('Sync %s', len(invalid))
        client.write(int4_to_str(len(invalid)))
        client.write(join_bytes(invalid))
        invalid.clear()

    #@asyncio.coroutine
    def handle_close(self, client, db_name):
        # X
        log.debug('Close %s' % db_name)
        if db_name in self.storages:
            self.storages[db_name].close()
            del self.storages[db_name]
            # Remove per-storage state for each client.
            for c in self.clients:
                del c.invalid[db_name]
                del c.unused_oids[db_name]
