# coding: UTF-8

from ctypes import c_char_p, c_int
from enum import IntEnum

from . import _libcgroup


class ErrorCode(IntEnum):
    NOTCOMPILED = 50000
    NOTMOUNTED = 50001
    NOTEXIST = 50002
    NOTCREATED = 50003
    SUBSYSNOTMOUNTED = 50004
    NOTOWNER = 50005
    MULTIMOUNTED = 50006

    NOTALLOWED = 50007
    MAXVALUESEXCEEDED = 50008
    CONTROLLEREXISTS = 50009
    VALUEEXISTS = 50010
    INVAL = 50011
    CONTROLLERCREATEFAILED = 50012
    FAIL = 50013
    NOTINITIALIZED = 50014
    VALUENOTEXIST = 50015

    OTHER = 50016
    NOTEQUAL = 50017
    CONTROLLERNOTEQUAL = 50018

    PARSEFAIL = 50019

    NORULES = 50020
    MOUNTFAIL = 50021

    EOF = 50023

    CONFIGPARSEFAIL = 50024
    NAMESPACEPATHS = 50025
    NAMESPACECONTROLLER = 50026
    MOUNTNAMESPACE = 50027
    UNSUPP = 50028
    CANTSETVALUE = 50029

    NONEMPTY = 50030

    @classmethod
    def from_param(cls, obj):
        return int(obj)


cgroup_strerror = _libcgroup.cgroup_strerror
cgroup_strerror.argtypes = (c_int,)
cgroup_strerror.restype = c_char_p

cgroup_get_last_errno = _libcgroup.cgroup_get_last_errno
cgroup_get_last_errno.argtypes = tuple()
cgroup_get_last_errno.restype = c_int
