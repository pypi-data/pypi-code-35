import socket
import sys

class DAC:
    def __init__(self, host="dac.nic.uk", port=3043):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def connect(self):
        self.socket.connect((self.host, self.port))

    def query_domain(self, domain):
        self.socket.send(("{}\r\n").format(domain).encode('utf-8'))
        response = self.socket.recv(1024)
        result = response.decode('utf-8').split(',')
        if len(result) == 2:
            return {'domain': domain,
                    'registered': False}
        elif len(result) == 6:
            domain,registered,detagged,created,expiry,tag = result
            return {'domain': domain,
                    'registered': registered == 'Y',
                    'detagged': detagged == 'Y',
                    'created': created,
                    'expiry': expiry,
                    'tag': tag}
        else:
            return {'domain': domain, 'unparsable': result}
