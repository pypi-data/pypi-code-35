import socket
import logging

class StatsdSender(object):
    def __init__(self, host, port):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        self.dest = (host, port)

    def send(self, data):
        logging.debug("Sending data: %s", data)
        self.sock.sendto(data.encode(), self.dest)
