# coding: utf8
from functools import partial

class cached_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, type):
        res = instance.__dict__[self.func.__name__] = self.func(instance)
        return res

curry = partial

