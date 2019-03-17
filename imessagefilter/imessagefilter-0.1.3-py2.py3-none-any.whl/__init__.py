#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from ctypes import windll


class CMessageFilter(object):

    msgfilter = None

    @classmethod
    def register(cls):
        if cls.msgfilter is None:
            filename = os.path.join(os.path.dirname(__file__), 'msgfilter.dll')
            cls.msgfilter = windll.LoadLibrary(os.path.normpath(filename))
        cls.msgfilter.register_message_filter()

    @classmethod
    def revoke(cls):
        if cls.msgfilter:
            cls.msgfilter.revoke_message_filter()


if __name__ == '__main__':
    windll.ole32.CoInitialize(0)
    CMessageFilter.Register()
    CMessageFilter.Revoke()
    windll.ole32.CoUninitialize()
