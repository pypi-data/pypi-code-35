#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

from requests.auth import HTTPBasicAuth
import json
import requests
import base64
import time
import os
import configparser
import sys

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

    def get_file(self, owner, repository, path, ref='master'):
        '''
        获取文件
        https://developer.github.com/v3/repos/contents/#get-contents
        '''

        url = '/repos/{}/{}/contents/{}'.format(owner, repository, path)
        self._get(url, ref=ref)
        is_success = self.response.status_code == 200
        return is_success, self.response.json()

    def create_from_file(self, owner, repository, filepath, path=None, sha=None):
        '''
        创建文件
        https://developer.github.com/v3/repos/contents/#create-a-file
        '''
        if not path:
            path = os.path.basename(filepath)

        content = ""
        with open(filepath, 'rb') as f:
            byte_data = f.read()
            content = base64.b64encode(byte_data).decode()

        url = '/repos/{}/{}/contents/{}'.format(owner, repository, path)
        data = {
            "message": "Create file {}".format(path),
            "author": {
                "name": self.author.name,
                "email": self.author.email
                },
            "content": content
            }
        if sha:
            data['sha'] = sha
        self._put(url, **data)
        return self.response.status_code, self.response.json()

    def create_repository(self, name, description="", homepage="",
            private=False, has_issues = True, has_projects = True,
            has_wiki = True, **kw
        ):
        '''
        创建仓库 https://developer.github.com/v3/repos/#create
        '''
        all_args = locals()
        url = '/user/repos'
        all_args.pop('self')
        self._post(url, **all_args)
        success = self.response.status_code == 201
        return success, self.response.json()

    def create_organization_repository(self, organization, name,
            description="", homepage="", private=False, has_issues = True,
            has_projects = True, has_wiki = True, **kw
        ):
        '''
        创建组织仓库 https://developer.github.com/v3/repos/#create
        '''
        all_args = locals()
        url = '/orgs/{}/repos'.format(organization)
        all_args.pop('self')
        self._post(url, **all_args)
        success = self.response.status_code == 201
        return success, self.response.json()

    def _get(self, url, **kw):
        res = requests.get(
            API_URL.format(url),
            params=kw,
            headers={"Accept": ACCEPT},
            auth=HTTPBasicAuth(self.user, self.password)
        )
        #  print(res.status_code)
        #  print(res.json())
        self.response = res

    def _put(self, url, **kw):
        res = requests.put(
            API_URL.format(url),
            json=kw,
            headers={"Accept": ACCEPT},
            auth=HTTPBasicAuth(self.user, self.password)
        )
        #  print(res.status_code)
        #  print(res.json())
        self.response = res

    def _post(self, url, **kw):
        res = requests.post(
            API_URL.format(url),
            json=kw,
            headers={"Accept": ACCEPT},
            auth=HTTPBasicAuth(self.user, self.password)
        )
        self.response = res
        #  print(res.status_code)
        #  print(res.json())

if __name__ == "__main__":
    config_path = '{}/.config/gos/config'.format(os.getenv("HOME"))
    credential_path = '{}/.config/gos/credentials'.format(os.getenv("HOME"))

    credential = configparser.ConfigParser()
    credential.read(credential_path)
    default_cred = credential['default']

    g = Github(default_cred['user'], default_cred['password'])

    config = configparser.ConfigParser()
    config.read(config_path)
    author = config['user']
    g.set_author(author['name'], author['email'])

    owner = config['repository']['owner']
    repo = config['repository']['repo']
    #  g.create_from_file('image', '/Users/wxnacy/Downloads/mac-font2.png',
            #  'common/{}'.format(time.time()))

    #  g.create_repository('test2')
    #  g.create_organization_repository(, 'test3')
    g.get_file('wxnacy', 'image', 'push')

