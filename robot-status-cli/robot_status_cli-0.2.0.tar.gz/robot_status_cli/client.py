from datetime import datetime

import requests

from .base import generate_token


class Client:

    def __init__(self, secret_key, server_url):
        self._secret_key = secret_key
        self.server_url = server_url

    def post(self, url, data, public_key):
        headers = self.get_headers(public_key, data)
        return requests.post(url, data, headers=headers, timeout=10)

    def get(self, url, public_key):
        headers = self.get_headers(public_key, method="GET")
        return requests.get(url, headers=headers, timeout=10)

    def get_headers(self, public_key, data=None, method="POST"):
        headers = {'public_key': public_key}
        if method == "GET":
            data = {"timestamp": datetime.utcnow().isoformat()}
            headers.update({
                "timestamp": data["timestamp"]
            })
        token = "bearer {0}".format(generate_token(self._secret_key, data))
        headers.update({
            "Authorization": token
        })
        return headers
