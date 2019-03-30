# -*- coding: utf-8 -*-

import sys

try:
    import configparser
except ImportError:  # pragma: no-cover
    import ConfigParser as configparser

try:
    import collections as userdict
except ImportError:  # pragma: no-cover
    import UserDict as userdict


UserDict = userdict.UserDict
PY2 = sys.version_info[0] == 2

if PY2:
    byteview = memoryview.tobytes
    StringLike = basestring if PY2 else str  # noqa: F821
    BytesLike = str
    ConfigParser = configparser.SafeConfigParser  # noqa: F821
else:
    def byteview(m):
        return m

    StringLike = str
    BytesLike = (bytes, memoryview)
    ConfigParser = configparser.ConfigParser
