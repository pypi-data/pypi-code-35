# coding: UTF-8

from ctypes import CFUNCTYPE, c_char_p, c_int, c_void_p
from enum import IntEnum

from . import _libcgroup


class LogLevel(IntEnum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4

    @classmethod
    def from_param(cls, obj):
        return int(obj)


cgroup_logger_callback = CFUNCTYPE(c_void_p, c_int, c_char_p, c_void_p)
# typedef void (*cgroup_logger_callback)(void *userdata, int level, const char *fmt, va_list ap);

cgroup_set_logger = _libcgroup.cgroup_set_logger
cgroup_set_logger.argtypes = (cgroup_logger_callback, c_int, c_void_p)
cgroup_set_logger.restype = None
# extern void cgroup_set_logger(cgroup_logger_callback logger, int loglevel, void *userdata);

cgroup_set_default_logger = _libcgroup.cgroup_set_default_logger
cgroup_set_default_logger.argtypes = (c_int,)
cgroup_set_default_logger.restype = None
# extern void cgroup_set_default_logger(int loglevel);

cgroup_set_loglevel = _libcgroup.cgroup_set_loglevel
cgroup_set_loglevel.argtypes = (c_int,)
cgroup_set_loglevel.restype = None
# extern void cgroup_set_loglevel(int loglevel);

cgroup_log = _libcgroup.cgroup_log
cgroup_log.argtypes = (c_int, c_char_p, c_void_p)
cgroup_log.restype = None
# extern void cgroup_log(int loglevel, const char *fmt, ...);

cgroup_parse_log_level_str = _libcgroup.cgroup_parse_log_level_str
cgroup_parse_log_level_str.argtypes = (c_char_p,)
cgroup_parse_log_level_str.restype = c_int
# extern int cgroup_parse_log_level_str(const char *levelstr);
