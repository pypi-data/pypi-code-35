name = "esenin_python"

import requests

class Client:
    def __init__(self, ip="localhost", port="9000"):
        self.ip = ip
        self.port = port

    def get_pos(self, text):
        r = requests.post("http://{}:{}/nlp/pos".format(self.ip, self.port), json = {"string": text})
        try:
            res = r.json()
        except ValueError:
            raise ValueError("Wrong format from server. Check your server status.")
        return res

