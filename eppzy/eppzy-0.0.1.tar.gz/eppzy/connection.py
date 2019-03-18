import socket
import ssl
from contextlib import contextmanager
from struct import pack, unpack


class LengthPrefixed:
    def __init__(self, s):
        self._s = s

    def send(self, b):
        b = pack("!i", len(b)) + b
        self._s.send(b)

    def recv(self):
        l, = unpack("!i", self._s.recv(4))
        return self._s.recv(l)


@contextmanager
def connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    ss = ssl.wrap_socket(s)
    ss.connect((host, port))
    try:
        yield LengthPrefixed(ss)
    finally:
        ss.close()
