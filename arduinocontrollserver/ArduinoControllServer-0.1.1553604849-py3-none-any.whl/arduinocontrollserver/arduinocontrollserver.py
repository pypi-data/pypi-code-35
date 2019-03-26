import json
import logging
import os
import re

try:
    # python 2
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer as BaseHTTPServer
except ImportError:
    # python 3
    from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler



class BasicRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, arduino_controll_server,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.arduino_controll_server = arduino_controll_server

    def translate_path(self, path):
        for regpath,rh in self.arduino_controll_server.requesthandler.items():
            if re.match(regpath, path):
                return rh.translate_path(self, path)

        return SimpleHTTPRequestHandler.translate_path(self, path)

class ArduinoControllServer():

    def __init__(self,port=80, socketport=8888, **kwargs):
        self.socketport = socketport
        self.port = port
        self.requesthandler={}

        if "www-data" in kwargs:
            self.WWW_DATA_DIR = os.path.abspath(kwargs['www-data'])
            del kwargs['www-data']
        else:
            self.WWW_DATA_DIR = os.path.join(os.path.expanduser('~'), "www-data")
            os.makedirs(self.WWW_DATA_DIR, exist_ok=True)

        os.chdir(self.WWW_DATA_DIR)

        if "logger" in kwargs:
            self.logger = kwargs['logger']
            del kwargs['logger']
        else:
            self.logger = logging.getLogger("arduinocontrollserver")

        with open("serverdata.js", "w+") as file:
            file.write("var serverdata = " + json.dumps(kwargs) + ";")

    def start(self):
        httpd = BaseHTTPServer(("", self.port), lambda *args,**kwargs: BasicRequestHandler(arduino_controll_server=self))
        self.logger.info("serving at port" + str(self.port))
        httpd.serve_forever()

if __name__ == "__main__":
    server = ArduinoControllServer(port=80,socketport=8888)
    server.start()

