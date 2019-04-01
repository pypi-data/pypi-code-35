#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   Request.py
Author: Lijiacai (1050518702@qq.com)
Date: 2018-11-20
Description:
    The crawler crawls requests, which mainly extend the retry mechanism, 
    can retry the connection for the proxy cause the connection failure.
    And if the same page needs cookie and access, the same spider can be used.
"""
import logging
import os
import random
import sys
import time
import requests
from requests import Response


class Request(object):
    """Request"""

    def __init__(self, proxies=None, try_time=5, frequence=0.1, timeout=20):
        """
        :param proxies: proxy agent
        :param try_time: retry count
        :param frequence: grasping frequency
        :param timeout: timeout
        """
        self.proxies = proxies
        self.session = requests.Session()
        self.try_time = try_time
        self.frequence = frequence
        self.timeout = timeout

    def proxy(self):
        """
        get proxy
        If there are other agents, change the function here.
        :return: return a ip：12.23.88.23:2345
        """
        if not self.proxies:
            one_proxy = None
        elif type(self.proxies) == list:
            one_proxy = random.choice(self.proxies)
        else:
            one_proxy = None
        #if one_proxy == None:
            #logging.info("self ip")
        return one_proxy

    def request(self, method, url, response_status="500",
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
                Returns :class:`Response <Response>` object.

                :param method: method for the new :class:`Request` object.
                :param url: URL for the new :class:`Request` object.
                :param response_status: response_status for the new :class:`response` object.
                :param params: (optional) Dictionary or bytes to be sent in the query
                    string for the :class:`Request`.
                :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                    object to send in the body of the :class:`Request`.
                :param json: (optional) json to send in the body of the
                    :class:`Request`.
                :param headers: (optional) Dictionary of HTTP Headers to send with the
                    :class:`Request`.
                :param cookies: (optional) Dict or CookieJar object to send with the
                    :class:`Request`.
                :param files: (optional) Dictionary of ``'filename': file-like-objects``
                    for multipart encoding upload.
                :param auth: (optional) Auth tuple or callable to enable
                    Basic/Digest/Custom HTTP Auth.
                :param timeout: (optional) How long to wait for the server to send
                    data before giving up, as a float, or a :ref:`(connect timeout,
                    read timeout) <timeouts>` tuple.
                :type timeout: float or tuple
                :param allow_redirects: (optional) Set to True by default.
                :type allow_redirects: bool
                :param proxies: (optional) Dictionary mapping protocol or protocol and
                    hostname to the URL of the proxy.
                :param stream: (optional) whether to immediately download the response
                    content. Defaults to ``False``.
                :param verify: (optional) Either a boolean, in which case it controls whether we verify
                    the server's TLS certificate, or a string, in which case it must be a path
                    to a CA bundle to use. Defaults to ``True``.
                :param cert: (optional) if String, path to ssl client cert file (.pem).
                    If Tuple, ('cert', 'key') pair.
                :rtype: requests.Response
                """
        for try_time in range(self.try_time):
            one_proxy_ = self.proxy()
	    one_proxy = one_proxy_
	    if one_proxy == None:
		pass
		#logging.info("ip-->None")
	    else:
		#logging.info("ip-->%s" % one_proxy)
                one_proxy = {"http": "http://%s" % one_proxy, "https": "http://%s" % one_proxy}
		
            try:
                response = self.session.request(method, url,
                                                params=params, data=data, headers=headers,
                                                cookies=cookies,
                                                files=files,
                                                auth=auth, timeout=timeout,
                                                allow_redirects=allow_redirects,
                                                proxies=one_proxy,
                                                hooks=hooks, stream=stream, verify=verify,
                                                cert=cert,
                                                json=json)
                if str(response.status_code) > response_status:
                    #logging.info("response status:[%s]" % str(response.status_code))
                    continue
		response.proxy = one_proxy_
                return response
            except Exception as e:
		pass
                #logging.exception("%s network error:%s" % (time.asctime(), str(e)))
            time.sleep(self.frequence)
	response = Response()
	response.proxy = "Response Error"
	return response
	

    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('DELETE', url, **kwargs)


def test():
    """unittest"""
    spider = Request(proxies=[])
    res = (spider.get(url="https://www.baidu.com"))
    print(res)
    print(res.proxy)


if __name__ == '__main__':
    test()
