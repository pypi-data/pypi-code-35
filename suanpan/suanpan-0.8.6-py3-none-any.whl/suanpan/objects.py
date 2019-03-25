# coding=utf-8
from __future__ import print_function

from addict import Dict


class HasName(object):
    @property
    def name(self):
        return self.__class__.__name__


class Context(Dict, HasName):
    pass


class Global(Context):
    pass
