# coding: UTF-8

import os
import unittest
from ctypes import POINTER, byref, c_char_p, c_int, c_long, c_void_p, cast

from libcgroup_bind.error import cgroup_strerror
from libcgroup_bind.groups import (
    cgroup_add_controller, cgroup_create_cgroup, cgroup_free, cgroup_new_cgroup, cgroup_set_uid_gid
)
from libcgroup_bind.init import cgroup_init
from libcgroup_bind.log import LogLevel, cgroup_logger_callback, cgroup_set_logger
from libcgroup_bind.tasks import DaemonType, cgroup_change_cgroup_path, cgroup_register_unchanged_process


def print_log(userdata: c_void_p, level: c_int, fmt: c_char_p, ap: c_void_p) -> None:
    print(level)
    print(fmt)
    c_long_p = POINTER(c_long)
    ap = cast(ap, c_long_p)
    value1 = cast(ap[0], c_char_p)
    print(value1)


class TestContext(unittest.TestCase):
    def test_init(self):
        cgroup_set_logger(cgroup_logger_callback(print_log), LogLevel.DEBUG, None)

        ret = cgroup_init()
        self.assertEqual(0, ret)

    # def test_create(self):
    #     ret = cgroup_init()
    #     self.assertEqual(0, ret)
    #
    #     cgroup = cgroup_new_cgroup(b'test')
    #     self.assertIsNotNone(cgroup)
    #
    #     uid = os.geteuid()
    #     gid = os.getegid()
    #     ret = cgroup_set_uid_gid(cgroup, uid, gid, uid, gid)
    #     self.assertEqual(0, ret, f'{cgroup_strerror(ret).decode()}')
    #
    #     cgroup_controller = cgroup_add_controller(cgroup, b'cpuset')
    #     self.assertIsNotNone(cgroup_controller)
    #
    #     ret = cgroup_create_cgroup(cgroup, 0)
    #     self.assertEqual(0, ret, f'{cgroup_strerror(ret).decode()}')
    #
    #     pid = os.getpid()
    #
    #     arr_t = c_char_p * 1
    #     cgroup_register_unchanged_process(pid, DaemonType.UNCHANGE_CHILDREN)
    #     ret = cgroup_change_cgroup_path(b'test', pid, arr_t(b'cpuset'))
    #     self.assertEqual(0, ret, f'{cgroup_strerror(ret).decode()}')
    #
    #     cgroup_free(byref(cgroup))


if __name__ == '__main__':
    unittest.main()
