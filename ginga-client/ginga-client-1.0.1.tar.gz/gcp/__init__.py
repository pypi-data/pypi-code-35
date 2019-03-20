# -*- coding: utf-8 -*-

import time
import json
import hashlib
import logging
import socket
import uuid

TCP_BUF_SIZE = 8192

logger = logging.getLogger('ginga')


class Client(object):
    def __init__(self, token, host, port, nonce):
        self.token = token
        self.host = host
        self.port = port
        self.nonce = nonce
        self.conn = None

    def lock(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((self.host, self.port))
        data = {
            'timestamp': int(time.time()),
            'nonce': str(uuid.uuid4()),
            'lock': True,
        }

        data['signature'] = self.sign(data)

        c.sendall(json.dumps(data))

        buf = c.recv(TCP_BUF_SIZE)
        data = json.loads(buf)
        if self.check_sign(data) is False:
            raise Exception('signature error')

        if data.get('lock') is False:
            raise Exception('this is unlock session')

        self.conn = c

    def unlock(self):
        if self.conn is None:
            return
        try:
            data = {
                'timestamp': int(time.time()),
                'nonce': str(uuid.uuid4()),
                'lock': False,
            }
            data['signature'] = self.sign(data)

            self.conn.send(json.dumps(data))
        finally:
            self.conn.close()

    def check_sign(self, data):
        if self.sign(data) == data.get('signature'):
            return True
        else:
            return False

    def sign(self, data):
        sl = [str(data.get('timestamp', '')), data.get('nonce', ''), self.token]
        sl.sort()
        sl = ''.join(sl)
        return hashlib.sha1(sl).hexdigest()
