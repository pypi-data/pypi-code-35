# coding: UTF-8

import subprocess
from ctypes import POINTER, Structure, c_char, c_char_p, c_int, c_short, c_uint, c_void_p
from enum import IntEnum

from . import _libcgroup

try:
    MAX_PATH = int(subprocess.check_output(['getconf', 'PATH_MAX', '/']))
except (ValueError, subprocess.CalledProcessError, OSError):
    MAX_PATH = 4096


class WalkType(IntEnum):
    PRE_DIR = 1
    POST_DIR = 2

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class FileType(IntEnum):
    FILE = 0
    DIR = 1
    OTHER = 2


class FileInfo(Structure):
    _fields_ = (
        ('type', c_uint),
        ('path', c_char_p),
        ('parent', c_char_p),
        ('full_path', c_char_p),
        ('depth', c_short),
    )


c_void_pp = POINTER(c_void_p)
c_int_p = POINTER(c_int)
FileInfoPointer = POINTER(FileInfo)

cgroup_walk_tree_begin = _libcgroup.cgroup_walk_tree_begin
cgroup_walk_tree_begin.argtypes = (c_char_p, c_char_p, c_int, c_void_pp, FileInfoPointer, c_int_p)
cgroup_walk_tree_begin.restype = c_int

cgroup_walk_tree_next = _libcgroup.cgroup_walk_tree_next
cgroup_walk_tree_next.argtypes = (c_int, c_void_pp, FileInfoPointer, c_int)
cgroup_walk_tree_next.restype = c_int

cgroup_walk_tree_end = _libcgroup.cgroup_walk_tree_end
cgroup_walk_tree_end.argtypes = (c_void_pp,)
cgroup_walk_tree_end.restype = c_int

cgroup_walk_tree_set_flags = _libcgroup.cgroup_walk_tree_set_flags
cgroup_walk_tree_set_flags.argtypes = (c_void_pp, c_int)
cgroup_walk_tree_set_flags.restype = c_int

cgroup_read_value_begin = _libcgroup.cgroup_read_value_begin
cgroup_read_value_begin.argtypes = (c_char_p, c_char_p, c_char_p, c_void_pp, c_char_p, c_int)
cgroup_read_value_begin.restype = c_int

cgroup_read_value_next = _libcgroup.cgroup_read_value_next
cgroup_read_value_next.argtypes = (c_void_pp, c_char_p, c_int)
cgroup_read_value_next.restype = c_int

cgroup_read_value_end = _libcgroup.cgroup_read_value_end
cgroup_read_value_end.argtypes = (c_void_pp,)
cgroup_read_value_end.restype = c_int


class Stat(Structure):
    _fields_ = (
        ('name', c_char * MAX_PATH),
        ('value', c_char * MAX_PATH),
    )


StatPointer = POINTER(Stat)

cgroup_read_stats_begin = _libcgroup.cgroup_read_stats_begin
cgroup_read_stats_begin.argtypes = (c_char_p, c_char_p, c_void_pp, StatPointer)
cgroup_read_stats_begin.restype = c_int

cgroup_read_stats_next = _libcgroup.cgroup_read_stats_next
cgroup_read_stats_next.argtypes = (c_void_pp, StatPointer)
cgroup_read_stats_next.restype = c_int

cgroup_read_stats_end = _libcgroup.cgroup_read_stats_end
cgroup_read_stats_end.argtypes = (c_void_pp,)
cgroup_read_stats_end.restype = c_int

cgroup_get_task_begin = _libcgroup.cgroup_get_task_begin
cgroup_get_task_begin.argtypes = (c_char_p, c_char_p, c_void_pp, c_int)
cgroup_get_task_begin.restype = c_int

cgroup_get_task_next = _libcgroup.cgroup_get_task_next
cgroup_get_task_next.argtypes = (c_void_pp, c_int)
cgroup_get_task_next.restype = c_int

cgroup_get_task_end = _libcgroup.cgroup_get_task_end
cgroup_get_task_end.argtypes = (c_void_pp,)
cgroup_get_task_end.restype = c_int


class MountPoint(Structure):
    _fields_ = (
        ('name', c_char * MAX_PATH),
        ('path', c_char * MAX_PATH),
    )


MountPointPointer = POINTER(MountPoint)

cgroup_get_controller_begin = _libcgroup.cgroup_get_controller_begin
cgroup_get_controller_begin.argtypes = (c_void_pp, MountPointPointer)
cgroup_get_controller_begin.restype = c_int

cgroup_get_controller_next = _libcgroup.cgroup_get_controller_next
cgroup_get_controller_next.argtypes = (c_void_pp, MountPointPointer)
cgroup_get_controller_next.restype = c_int

cgroup_get_controller_end = _libcgroup.cgroup_get_controller_end
cgroup_get_controller_end.argtypes = (c_void_pp,)
cgroup_get_controller_end.restype = c_int


class ControllerData(Structure):
    _fields_ = (
        ('name', c_char * MAX_PATH),
        ('hierarchy', c_int),
        ('num_cgroups', c_int),
        ('enabled', c_int),
    )


ControllerDataPointer = POINTER(ControllerData)

cgroup_get_all_controller_begin = _libcgroup.cgroup_get_all_controller_begin
cgroup_get_all_controller_begin.argtypes = (c_void_pp, ControllerDataPointer)
cgroup_get_all_controller_begin.restype = c_int

cgroup_get_all_controller_next = _libcgroup.cgroup_get_all_controller_next
cgroup_get_all_controller_next.argtypes = (c_void_pp, ControllerDataPointer)
cgroup_get_all_controller_next.restype = c_int

cgroup_get_all_controller_end = _libcgroup.cgroup_get_all_controller_end
cgroup_get_all_controller_end.argtypes = (c_void_pp,)
cgroup_get_all_controller_end.restype = c_int

cgroup_get_subsys_mount_point_begin = _libcgroup.cgroup_get_subsys_mount_point_begin
cgroup_get_subsys_mount_point_begin.argtypes = (c_char_p, c_void_pp, c_char_p)
cgroup_get_subsys_mount_point_begin.restype = c_int

cgroup_get_subsys_mount_point_next = _libcgroup.cgroup_get_subsys_mount_point_next
cgroup_get_subsys_mount_point_next.argtypes = (c_void_pp, c_char_p)
cgroup_get_subsys_mount_point_next.restype = c_int

cgroup_get_subsys_mount_point_end = _libcgroup.cgroup_get_subsys_mount_point_end
cgroup_get_subsys_mount_point_end.argtypes = (c_void_pp,)
cgroup_get_subsys_mount_point_end.restype = c_int
