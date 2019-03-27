import json
import time

import urllib3


class DrongoClient(object):
    def __init__(self, api_url):
        self.http = urllib3.PoolManager(32)

        self.api_url = api_url
        self.headers = {'connection': 'keep-alive'}
        self._retries = 3
        self._retry_wait_time = 1

    def _request(self, *args, **kwargs):
        for _ in range(self._retries):
            try:
                return self.http.request(*args, **kwargs)
            except Exception:
                time.sleep(self._retry_wait_time)

    def _response(self, resp):
        if resp.headers['Content-Type'] == 'application/json':
            return json.loads(resp.data.decode('utf-8'))
        else:
            return resp.data

    def get(self, url, params=None, headers=None):
        url = self.api_url + url
        h = {}
        h.update(self.headers)
        if headers is not None:
            h.update(headers)
        r = self._request('GET', url, params, headers=h)
        return self._response(r)

    def get_download(self, url, fd, headers=None):
        url = self.api_url + url
        h = {}
        h.update(self.headers)
        if headers is not None:
            h.update(headers)
        r = self._request(
            'GET',
            url,
            headers=h,
            preload_content=False
        )
        while True:
            data = r.read(10240)
            if not data:
                break
            fd.write(data)

    def post_json(self, url, payload, headers=None):
        url = self.api_url + url
        h = {'content-type': 'application/json'}
        h.update(self.headers)
        if headers is not None:
            h.update(headers)
        r = self._request(
            'POST',
            url,
            body=json.dumps(payload).encode('utf-8'),
            headers=h
        )
        return self._response(r)

    def post_form(self, url, fields, headers=None):
        url = self.api_url + url
        h = {}
        h.update(self.headers)
        if headers is not None:
            h.update(headers)
        r = self._request(
            'POST',
            url,
            fields=fields,
            headers=h
        )
        return self._response(r)

    def put_json(self, url, payload, headers=None):
        url = self.api_url + url
        h = {'content-type': 'application/json'}
        h.update(self.headers)
        if headers is not None:
            h.update(headers)
        r = self._request(
            'PUT',
            url,
            body=json.dumps(payload).encode('utf-8'),
            headers=h
        )
        return self._response(r)

    def delete(self, url, params=None, headers=None):
        url = self.api_url + url
        h = {}
        h.update(self.headers)
        if headers is not None:
            h.update(headers)
        r = self._request(
            'DELETE',
            url,
            params,
            headers=h)
        return self._response(r)

    def set_header(self, key, val):
        self.headers[key] = val

    def remove_header(self, key):
        if key in self.headers:
            self.headers.pop(key)
