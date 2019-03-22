import sys
import telnetlib

class Client():

    def __init__(self, ip, port, username, password):

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

tn = telnetlib.Telnet("10.0.0.138")
