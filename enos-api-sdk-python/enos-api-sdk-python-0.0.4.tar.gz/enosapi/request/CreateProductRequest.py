# coding: utf8
# Author:xuyang.li
# Date:2018/11/20
"""
    create product request
"""
from enosapi.request.EnOSRequest import EnOSRequest
from enosapi.util.const import Const
import json


class CreateProductRequest(EnOSRequest):

    __url = '/connectService/products'
    __type = Const.request_post
    __context_type = 'application/json'

    def __init__(self, org_id, params):
        self.org_id = org_id
        self.payload = params
        self.params = {}

    def get_request_url(self):
        return self.__url

    def get_request_type(self):
        return self.__type

    def get_content_type(self):
        return self.__context_type

    def get_params(self):
        return self.params

    def get_context_body(self):
        return json.dumps(self.payload)

    def replace_params(self):
        return True

    def get_replace_params(self):
        return self.payload
