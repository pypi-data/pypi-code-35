import socket
import select
import logging

class StatsdListener(object):
    def __init__(self, port, mangler):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        self.sock.bind(("", port))
        self.mangler = mangler

    def listen(self):
        logging.debug("Starting listener")
        while True:
            ready = select.select([self.sock], [], [], 1)
            if ready[0]:
                data = self.sock.recv(4096)
                self.mangler.mangle(data.decode().strip())
