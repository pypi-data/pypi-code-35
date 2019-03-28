# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64
import hashlib
import hmac
import time

from . import compat

SELF_DEFINE_HEADER_PREFIX = "x-gd-"
SELF_DEFINE_AUTH_PREFIX = "GeneDock"


def format_header(headers=None):
    """
    format the headers that self define
    convert the self define headers to lower.
    """
    if not headers:
        headers = {}
    tmp_headers = {}

    for k in headers.keys():
        tmp_str = compat.to_bytes(headers[k])

        if k.lower().startswith(SELF_DEFINE_HEADER_PREFIX):
            k_lower = k.lower().strip()
            tmp_headers[k_lower] = tmp_str
        else:
            tmp_headers[k.strip()] = tmp_str
    return tmp_headers


def extract_resource_from_url(url):
    if url.lower().startswith("http://"):
        idx = url.find('/', 7, -1)
        return url[idx:].strip()
    elif url.lower().startswith("https://"):
        idx = url.find('/', 8, -1)
        return url[idx:].strip()
    else:
        return url.strip()


def canonicalize_resource(resource):
    normal_resource = compat.urlunquote(resource)  # 将 %xx 替换为单字符。abc%27 -> abc/
    res_list = normal_resource.split("?")
    if len(res_list) <= 1 or len(res_list) > 2:
        return normal_resource
    res = res_list[0]
    param = res_list[1]
    params = param.split("&")
    params = sorted(params)
    param = '&'.join(params)
    return res + "?" + param


class GeneDockAuth(object):
    """ This class is using for sending GeneDock API by add authentication """

    def __init__(self, access_key_id, access_key_secret, verbose=True):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.verbose = verbose

    def __call__(self, r):
        method = r.method
        content_type = r.headers.get('Content-Type', '')
        content_md5 = r.headers.get('Content-MD5', '')
        canonicalized_gd_headers = ""
        date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

        resource = extract_resource_from_url(r.url)

        tmp_headers = format_header(r.headers)
        if len(tmp_headers) > 0:
            x_header_list = list(tmp_headers.keys())
            x_header_list.sort()
            for k in x_header_list:
                if k.startswith(SELF_DEFINE_HEADER_PREFIX):
                    canonicalized_gd_headers += "%s:%s\n" % (k, tmp_headers[k])

        canonicalized_resource = canonicalize_resource(resource)

        string_to_sign = "{method}\n{content_md5}\n{content_type}\n{date}\n{gd_headers}{resource}".format(
            method=method,
            content_md5=content_md5,
            content_type=content_type,
            date=date,
            gd_headers=canonicalized_gd_headers,
            resource=canonicalized_resource
        )

        h = hmac.new(compat.to_bytes(self.access_key_secret), compat.to_bytes(string_to_sign), hashlib.sha1)
        signature = base64.encodestring(h.digest()).strip()

        r.headers["Date"] = date
        r.headers["Authorization"] = "{prefix} {access_key_id}:{signature}".format(
            prefix=SELF_DEFINE_AUTH_PREFIX,
            access_key_id=self.access_key_id,
            signature=compat.to_string(signature))
        return r
