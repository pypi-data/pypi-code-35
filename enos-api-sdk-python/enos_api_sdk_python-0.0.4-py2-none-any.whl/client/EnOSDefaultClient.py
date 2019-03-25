# coding: utf8
# Author:xuyang.li
# EnOS API default client
import logging
import logging.config
import os
import sys

from enosapi.request.EnOSRequest import EnOSRequest
from enosapi.request.ApplyCertificateByDeviceKeyRequest import ApplyCertificateByDeviceKeyRequest
from enosapi.util.Sign import Sign
from enosapi.util.const import Const
import json
import time
import requests
if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.request as urllib2


class EnOSDefaultClient:
    __logging = logging.getLogger(__name__)

    def __init__(self, url, access_key, secret_key, timeout=30000):
        assert url is not None
        assert access_key is not None
        assert secret_key is not None

        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key
        self.timeout = timeout

        self.setupFileLogger('log.json')

    def execute(self, request):
        try:
            assert isinstance(request, EnOSRequest)
            if Const.request_get == request.get_request_type():
                return EnOSRequest.get_response(self.do_get(request))
            elif Const.request_post == request.get_request_type():
                return EnOSRequest.get_response(self.do_post(request))
            else:
                raise RuntimeError("Unsupported request types")
        except Exception as x:
            self.__logging.error(x)
            raise x

    def do_get(self, request):
        url = self.__get_base_url(request)
        param_str = ''
        params = request.get_params()
        if params is not None:
            assert isinstance(params, dict)
            for key in params:
                if "orgId" == key or "requestTimestamp" == key:
                    pass
                else:
                    param_str += "&"
                    param_str += key
                    param_str += "="
                    param_str += str(params[key])

        if len(param_str) > 0:
            url += param_str

        self.__logging.info("do get execute:%s", url)
        res = requests.get(url).content
        self.__logging.info("response :%s", res)
        return res

    def do_post(self, request):
        url = self.__get_base_url(request)
        data = request.get_params() if not request.replace_params() else request.get_replace_params()
        upload_file = getattr(request, 'upload_file') if hasattr(request, 'upload_file') else None
        self.__logging.info("do post execute:%s ", url)
        # speiaclly, as it need a string data, not json or map
        if isinstance(request, ApplyCertificateByDeviceKeyRequest):
            headers = request.get_headers()
            req = urllib2.Request(url, data=data.encode('utf8'), headers=headers)
            res = urllib2.urlopen(req, timeout=self.timeout).read()
        elif upload_file:
            res = requests.post(url, data=data, files=request.upload_file).content
        else:
            res = requests.post(url, json=data).content
        self.__logging.info("response :%s", res)
        return res

    @staticmethod
    def setupBasicLogger(level='INFO', filePath=None,
                         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
        if filePath is not None:
            logging.basicConfig(level=level, filename=filePath, format=format)
        else:
            logging.basicConfig(level=level, format=format)

    @staticmethod
    def setupFileLogger(filePath):
        path = filePath
        if os.path.exists(path):
            with open(path, "r") as f:
                config = json.load(f)
                logging.config.dictConfig(config)

    def __get_base_url(self, request):
        if self.url.endswith("/"):
            self.url = self.url[:-1]
        url = self.url + request.get_request_url()
        requestTimestamp = str(int(time.time() * 1000))
        params = request.get_params() if request.get_params() is not None else {}
        params["requestTimestamp"] = requestTimestamp
        params["orgId"] = request.org_id
        url = url + "?accessKey=" + self.access_key + "&requestTimestamp=" + requestTimestamp + "&orgId=" \
            + request.org_id + "&sign=" + Sign.sign(self.access_key,
                                                    self.secret_key,
                                                    params,
                                                    request.get_context_body())
        return url
