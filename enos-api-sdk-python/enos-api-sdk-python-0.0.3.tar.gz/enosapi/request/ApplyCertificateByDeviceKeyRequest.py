# coding: utf8
# Author:xuyang.li
# Date:2018/11/23
"""
"""
from enosapi.request.EnOSRequest import EnOSRequest
from enosapi.util.const import Const
import json


class ApplyCertificateByDeviceKeyRequest(EnOSRequest):

    __url = '/connectService/products/{productKey}/devices/{deviceKey}/certificates/apply'
    __type = Const.request_post
    __context_type = 'application/json;charset=UTF-8'

    def __init__(self, org_id, product_key, device_key, csr):
        self.org_id = org_id
        self.product_key = product_key
        self.device_key = device_key
        self.csr = csr
        self.params = {}

    def get_request_url(self):
        return self.__url.replace("{productKey}", self.product_key).replace("{deviceKey}", self.device_key)

    def get_request_type(self):
        return self.__type

    def get_content_type(self):
        return self.__context_type

    def get_context_body(self):
        return self.csr

    def get_params(self):
        return self.params

    def replace_params(self):
        return True

    def get_replace_params(self):
        return self.csr

    def get_headers(self):
        return {'content-type' : self.get_content_type()}

