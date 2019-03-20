import requests
from yarl import URL

from megaphone.errors import APIError, AuthenticationError

BASE_URL = "https://cms.megaphone.fm/api"


class IterListGetter:
    def __init__(self, client, response, parsed):
        self.client = client
        self.response = response
        self.result = parsed

    def __iter__(self):
        return self

    def __next__(self):
        if self.result:
            return self.result.pop()
        if "next" not in self.response.links:
            raise StopIteration
        url = URL(self.response.links['next']['url'])
        self.response = self.client.call('get', url, url.query)
        self.result = self.response.json()
        # there's a bug in the megaphone API where sometimes
        # a next Link is given but with no values
        if not self.result:
            raise StopIteration
        return self.result.pop()


class HTTPClient:
    def __init__(self, token, base_url=None):
        self.base_url = base_url or URL(BASE_URL)
        self.token = token
        self.headers = {'Authorization': 'Token token="%s"' % token}

    def call(self, method, url, args=None):
        url = url.with_query(args)
        resp = getattr(requests, method)(str(url), headers=self.headers)
        if resp.status_code == 401:
            raise AuthenticationError(resp.text)
        elif resp.status_code != 200:
            raise APIError(resp.text)
        return resp

    def get(self, *parts, **args):
        url = self.base_url / "/".join(parts)
        result = self.call('get', url, args)
        parsed = result.json()
        if isinstance(parsed, list):
            return IterListGetter(self, result, parsed)
        return parsed

    def __truediv__(self, path):
        return HTTPClient(self.token, self.base_url / path)


class APIObject:
    path = None

    @classmethod
    def build(klass, http, objid):
        return klass(http, {'id': objid}).refresh()

    def __init__(self, http, data):
        self.data = data
        self.http = http / self.__class__.path / self.id

    def refresh(self):
        self.data = self.http.get()
        return self

    def __getattr__(self, name):
        return self.data[name]

    def __str__(self):
        attrs = ["%s=%s" % (k, v) for k, v in self.data.items()]
        attrs = ", ".join(attrs)
        return "<%s %s>" % (self.__class__.__name__, attrs)
