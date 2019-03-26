import os
import json

class SSProfile(object):
    def __init__(self, fileName = None):
        self.config = {"server": "0.0.0.0", 
                       "timeout": 300,
                       "method": "aes-256-cfb"}
        self.ports = {}
        if fileName != None:
            self.load(fileName)

    def addPort(self, port, password):
        port = str(port)
        self.ports[port] = password

    def delPort(self, port):
        port = str(port)
        if self.ports.get(port) != None:
            self.ports.pop(port)

    def save(self, fileName):
        try:
            self.config["port_password"] = self.ports
            str   = json.dumps(self.config)
            index = fileName.rfind('/')
            path  = fileName[0:index+1]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(fileName, 'w+') as fd:
                fd.write(str)
        except:
            return False
        return True

    def load(self, fileName):
        try:
            str = None
            with open(fileName, 'r+') as fd:
                str = fd.read(str)
            value  = json.loads(str)
            ports  = value.get('port_password')
            server = value.get('server')
            time   = value.get('timeout')
            method = value.get('method')

            self.ports = ports
            if server != None:
                self.config['server'] = server
            if time != None:
                self.config['timeout'] = time
            if method != None:
                self.config['method'] = method
            return True
        except:
            return False




