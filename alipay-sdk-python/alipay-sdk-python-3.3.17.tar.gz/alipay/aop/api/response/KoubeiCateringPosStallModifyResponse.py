#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse


class KoubeiCateringPosStallModifyResponse(AlipayResponse):

    def __init__(self):
        super(KoubeiCateringPosStallModifyResponse, self).__init__()
        self._id = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def parse_response_content(self, response_content):
        response = super(KoubeiCateringPosStallModifyResponse, self).parse_response_content(response_content)
        if 'id' in response:
            self.id = response['id']
