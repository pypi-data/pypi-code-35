# -*- coding=utf-8 -*-
from requests import Session
from lxml import html


class BaseClient:
    def __init__(self):
        raise NotImplementedError

    def get(self, url):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def _get_doc(self):
        if self._tree is None:
            self._tree = html.fromstring(self._text)
        return self._tree

    def _set_doc(self, obj):
        self._tree = obj

    tree = property(_get_doc, _set_doc)


class RequestsSession(BaseClient):

    def __init__(self, user_agent=None, content_type=None):
        self._tree = None
        self._text = None
        self.sessions = Session()
        self.sessions.keep_alive = False
        self.sessions.adapters.DEFAULT_RETRIES = 5
        self.base_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        self.base_content_type = 'application/json;charset=utf-8'
        self.headers = {
            'User-Agent': user_agent or self.base_user_agent,
            'Content-Type': content_type or self.base_content_type
        }

    def get(self, url, headers=None, params=None):
        headers = headers or self.headers
        r = self.sessions.get(url, headers=headers,
                              params=params, verify=False)
        self._text = r.text
        return r

    def post(self, url, headers=None, data=None):
        headers = headers or self.headers
        return self.sessions.post(url, headers=headers, data=data)
