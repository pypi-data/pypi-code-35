#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from alipay.aop.api.response.AlipayResponse import AlipayResponse


class MybankCreditSupplychainTradeCancelResponse(AlipayResponse):

    def __init__(self):
        super(MybankCreditSupplychainTradeCancelResponse, self).__init__()
        self._ev_seq_no = None

    @property
    def ev_seq_no(self):
        return self._ev_seq_no

    @ev_seq_no.setter
    def ev_seq_no(self, value):
        self._ev_seq_no = value

    def parse_response_content(self, response_content):
        response = super(MybankCreditSupplychainTradeCancelResponse, self).parse_response_content(response_content)
        if 'ev_seq_no' in response:
            self.ev_seq_no = response['ev_seq_no']
