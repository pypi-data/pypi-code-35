# coding: UTF-8

from ctypes import CDLL
from ctypes.util import find_library

_libcgroup = CDLL(find_library('cgroup'), use_errno=True)
