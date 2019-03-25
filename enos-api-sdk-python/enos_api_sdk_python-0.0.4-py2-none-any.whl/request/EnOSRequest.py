# coding: utf8
# Author:xuyang.li
"""
    EnOS default client
"""
import json
from abc import ABCMeta, abstractmethod

from enosapi.response.EnOSResponse import EnOSResponse


class EnOSRequest:
    __metaclass__ = ABCMeta

    def __init__(self, org_id):
        self.org_id = org_id

    @abstractmethod
    def get_request_url(self):
        pass

    @abstractmethod
    def get_request_type(self):
        pass

    @abstractmethod
    def get_content_type(self):
        pass

    @abstractmethod
    def get_params(self):
        pass

    def replace_params(self):
        return False

    def get_context_body(self):
        return None

    @staticmethod
    def get_response(response_str):
        response_str = response_str.decode('utf8') if isinstance(response_str, bytes) else response_str
        jsonobject = json.loads(response_str)
        body = None
        msg = None
        if "body" in jsonobject:
            body = jsonobject["body"]
        if "msg" in jsonobject:
            msg = jsonobject["msg"]

        response = EnOSResponse(jsonobject["status"], jsonobject["requestId"],
                                jsonobject["submsg"], body,
                                jsonobject["data"], msg)
        return response
