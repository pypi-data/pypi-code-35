# -*- coding: utf-8 -*-

# @Date    : 2019-03-31
# @Author  : Peng Shiyu


"""
一个对 requests 的包装类，用法和requests 一模一样
"""
from __future__ import unicode_literals, print_function

import requests


class FakeRequests(object):
    """
    经常到处找请求头用户代理，这下一次解决完
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
    }

    @classmethod
    def request(cls, method, url, **kwargs):
        kwargs.setdefault("headers", cls.headers)
        response = requests.request(method, url, **kwargs)
        response.encoding = response.apparent_encoding
        return response

    @classmethod
    def get(cls, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return cls.request('get', url, params=params, **kwargs)

    @classmethod
    def post(cls, url, data=None, json=None, **kwargs):
        return cls.request('post', url, data=data, json=json, **kwargs)


if __name__ == '__main__':
    r = FakeRequests.get(url="https://httpbin.org/get")
    print(r.text)
