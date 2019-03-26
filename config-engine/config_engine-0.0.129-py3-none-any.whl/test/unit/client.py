import os
import requests


class Client:
    session = None
    server_url = None

    def __init__(self):
        self.server_url = os.environ.get('SERVER_URL', 'http://127.0.0.1:5015')
        self.session = requests.Session()
        self.static_headers = {}

    def get(self, path, **kwargs):
        return self.call('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.call('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self.call('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self.call('DELETE', path, **kwargs)

    def call(self, method, path, headers=None, **kwargs):
        headers = headers or {}
        headers.update(self.static_headers)
        return self.session.request(method, '{}{}'.format(self.server_url, path), headers=headers, **kwargs)


client = Client()
