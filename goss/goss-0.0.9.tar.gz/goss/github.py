#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from requests.auth import HTTPBasicAuth
from os import path
import json
import requests
import base64
import time

API_URL = 'https://api.github.com{}'
ACCEPT = 'application/vnd.github.v3+json'

class BaseObject(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return json.loads(self.to_json())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def __str__(self):
        return self.to_json()

class Content(BaseObject):
    pass



class Author():
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Response(BaseObject):
    def __init__(self):
        self.contents = []
    pass

class Github():
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def set_author(self, name, email):
        self.author = Author(name, email)

    def create_from_file(self, owner, repository, filepath, path=None):
        '''
        创建文件
        https://developer.github.com/v3/repos/contents/#create-a-file
        '''
        if not path:
            path = path.basename(filepath)

        content = ""
        with open(filepath, 'rb') as f:
            byte_data = f.read()
            content = base64.b64encode(byte_data).decode()

        url = '/repos/{}/{}/contents/{}'.format(owner, repository, path)
        self._put(url, **{
              "message": "Create file {}".format(path),
              "author": {
                    "name": self.author.name,
                    "email": self.author.email
                  },
                "content": content
                }
            )

        data = self.response.json()
        #  print(json.dumps(data, indent=4))
        f = Content(**data['content'])
        res = Response()
        res.contents.append(f)
        return res

    def _put(self, url, **kw):
        res = requests.put(
            API_URL.format(url),
            json=kw,
            headers={"Accept": ACCEPT},
            auth=HTTPBasicAuth(self.user, self.password)
        )
        self.response = res

if __name__ == "__main__":
    g = Github('', '')
    g.create_from_file('image', '/Users/wxnacy/Downloads/mac-font2.png',
            'common/{}'.format(time.time()))

