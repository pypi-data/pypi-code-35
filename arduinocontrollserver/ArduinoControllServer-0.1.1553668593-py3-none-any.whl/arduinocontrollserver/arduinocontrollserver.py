import json
import logging
import os
import re
import shutil

try:
    # python 2
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer as BaseHTTPServer
except ImportError:
    # python 3
    from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler



class BasicRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, arduino_controll_server, request, client_address, server):
        self.arduino_controll_server = arduino_controll_server
        super().__init__(request, client_address, server)


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

        if "www_data" in kwargs:
            self.WWW_DATA_DIR = os.path.abspath(kwargs['www_data'])
            del kwargs['www_data']
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
        httpd = BaseHTTPServer(("", self.port), lambda request, client_address, server: BasicRequestHandler(arduino_controll_server=self,request=request, client_address=client_address, server=server))
        self.logger.info("serving at port " + str(self.port))
        httpd.serve_forever()

    def get_www_data_path(self):
        from arduinocontrollserver import www_data
        return os.path.abspath(os.path.dirname(www_data.__file__))

    def deploy(self,path,parent=None):
        recursive_overwrite(os.path.abspath(path),os.path.abspath(os.path.join(self.WWW_DATA_DIR,parent if parent is not None else "")))

def recursive_overwrite(src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)

if __name__ == "__main__":
    server = ArduinoControllServer(port=80,socketport=8888)
    server.start()

