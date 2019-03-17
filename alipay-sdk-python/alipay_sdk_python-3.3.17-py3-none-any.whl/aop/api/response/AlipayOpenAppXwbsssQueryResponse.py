#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse


class AlipayOpenAppXwbsssQueryResponse(AlipayResponse):

    def __init__(self):
        super(AlipayOpenAppXwbsssQueryResponse, self).__init__()
        self._a = None

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    def parse_response_content(self, response_content):
        response = super(AlipayOpenAppXwbsssQueryResponse, self).parse_response_content(response_content)
        if 'a' in response:
            self.a = response['a']
