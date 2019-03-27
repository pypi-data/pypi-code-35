# -*- coding: utf-8 -*-

import json
import os
from zipfile import ZipFile


class EasyDict:
    """Easy used dict
    Example:
    >>> d = EasyDict(a=1, b=2)
    >>> d.a
    1
    >>> d.b
    2
    >>> d.c = 3
    >>> d.c
    3
    >>> str(d)
    '{"a": "1", "b": "2", "c": "3"}'
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattr__(self, item):
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __str__(self):
        _dict = {k: str(v) for k, v in self.__dict__.items()}
        return json.dumps(_dict)


def unzip(src: str, dest: str):
    if not os.path.isdir(dest):
        dest = os.path.dirname(dest)
    z_file = ZipFile(src)
    z_file.extractall(dest)
