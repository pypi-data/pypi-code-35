#!/usr/bin/python
# -*- coding: utf-8 -*-

class AccountAPI(object):

    def self_account(self):
        url = self.base_url + "accounts/me"
        contents = self.get(url)
        return contents

    def acl_account(self):
        url = self.base_url + "accounts/acl"
        contents = self.get(url)
        return contents
