# coding: utf8
# Author:xuyang.li
# Date:2018/11/22
"""
"""

from enosapi.request.EnOSRequest import EnOSRequest
from enosapi.util.const import Const


class PostMeasurepointsEnOSRequest(EnOSRequest):
    __url = '/connectService/products/{product_key}/devices/measurepoints'
    __type = Const.request_post
    __context_type = 'multipart/form-data;charset=UTF-8'

    def __init__(self, org_id, product_key, params, upload_file={'file':''.encode('utf8')}):
        assert product_key is not None
        self.org_id = org_id
        self.params = params
        self.upload_file = upload_file
        self.product_key = product_key

    def get_request_url(self):
        return self.__url.replace("{product_key}", self.product_key)

    def get_request_type(self):
        return self.__type

    def get_content_type(self):
        return self.__context_type

    def get_params(self):
        return self.params
