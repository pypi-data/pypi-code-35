# -*- coding: utf-8 -*-
"""Testing distributed systems."""
import re
import sys
import typing
from typing import Any, Mapping, NamedTuple, Sequence

__version__ = '0.0.1'
__author__ = 'Ask Solem'
__contact__ = 'ask@celeryproject.org'
__homepage__ = 'https://github.com/ask/livecheck'
__docformat__ = 'restructuredtext'

# -eof meta-


class version_info_t(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: str


# bumpversion can only search for {current_version}
# so we have to parse the version here.
_match = re.match(r'(\d+)\.(\d+).(\d+)(.+)?', __version__)
if _match is None:
    raise RuntimeError('VERSION HAS ILLEGAL FORMAT')
_temp = _match.groups()
VERSION = version_info = version_info_t(
    int(_temp[0]), int(_temp[1]), int(_temp[2]), _temp[3] or '', '')
del(_match)
del(_temp)
del(re)
