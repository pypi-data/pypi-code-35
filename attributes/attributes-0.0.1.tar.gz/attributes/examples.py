# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
# this is a example to use Attribute.
# ----------

from .core import Attribute

class info(Attribute):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    @classmethod
    def get_all(cls, obj, *, inherit=False):
        return Attribute.get_attrs(obj, info, inherit=inherit)

    @classmethod
    def get_all_as_dict(cls, obj, *, inherit=False):
        d = {}
        for attr in reversed(cls.get_all(obj, inherit=inherit)):
            # reversed so we can override parent.
            d[attr.name] = attr.value
        return d

    @classmethod
    def get_value(cls, obj, name, *, inherit=False):
        for attr in Attribute.get_attrs(obj, info, inherit=inherit):
            if attr.name == name:
                return attr.value
        return None
