# coding: UTF-8

from ctypes import POINTER, c_char_p, c_int

from . import _libcgroup

cgroup_init = _libcgroup.cgroup_init
cgroup_init.argtypes = tuple()
cgroup_init.restype = c_int

c_char_pp = POINTER(c_char_p)

cgroup_get_subsys_mount_point = _libcgroup.cgroup_get_subsys_mount_point
cgroup_get_subsys_mount_point.argtypes = (c_char_p, c_char_pp)
cgroup_get_subsys_mount_point.restype = c_int
