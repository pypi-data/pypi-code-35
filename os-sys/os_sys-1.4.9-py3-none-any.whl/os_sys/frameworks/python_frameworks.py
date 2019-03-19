import sys, os, string, abc, __future__
class str(str):
    def __init__(self):
        self.python_version = sys.version
        self.is_win = sys.getwindowsversion()
class list(list):
    def __init__(self):
        self.python_version = sys.version
        self.is_win = sys.getwindowsversion()
import http as _http, html as _html_
class __html():
    
    http = _http
    html = _html_
    def __init__(self, port="9752"):
        self.init = True
        self.html_version = "html5"
        self.http = True
        self.port = port
        self.html = _html_
        self.http = _http
        self.localhost = "http://127.0.0.1:"
        self.host = self.localhost + self.port


    



html = __html()

