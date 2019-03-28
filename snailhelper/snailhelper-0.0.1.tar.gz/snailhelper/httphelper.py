# -*- coding:utf-8 -*-
"""HTTP客户端助手"""
import re
import urllib
from snailhelper import cachehelper
from http import cookiejar


def get(url, data=None, header=None):
    return __http(url, data, header)


def post(url, data=None, header=None):
    return __http(url, data, header, 'POST')


def put(url, data=None, header=None):
    return __http(url, data, header, 'PUT')


def delete(url, data=None, header=None):
    return __http(url, data, header, 'DELETE')


def __http(url, data=None, header=None, method='GET'):

    host = re.findall(r'^https?://[^/]+', url, re.I)

    if host is None or len(host) != 1:
        raise Exception('URL异常！(url: %s)' % url)

    host = host[0]
    ckey = '__SNAIL_HTTPHELPER_CLIENT_[%s]__' % host

    client = cachehelper.get_local(ckey)

    if not client:
        cookie = cookiejar.CookieJar()
        client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # 缓存客户端
        cachehelper.put(ckey, client)

    if header is None:
        header = {}

    if data:
        if type(data) is dict:
            data = urllib.parse.urlencode(data).encode('utf-8')
        elif not type(data) is str:
            data = str(data)

    req = urllib.request.Request(url, data=data, headers=header, method=method)

    return client.open(req).read().decode('utf-8')








