import unittest
from ctypes import byref, c_void_p, create_string_buffer

from libcgroup_bind.error import ErrorCode
from libcgroup_bind.iterators import cgroup_get_subsys_mount_point_begin, cgroup_get_subsys_mount_point_next

from libcgroup import CGroup, _raise_error

PIDS = (3807, 3873, 7797)


class MyTestCase(unittest.TestCase):
    def test_0_root(self) -> None:
        CGroup.root: CGroup
        self.assertIsNotNone(CGroup.root)
        for controller in CGroup.root.controllers:
            print(controller)

    def test_something(self):
        cgroup = CGroup('test', 'cpuset', 'cpu')
        self.assertIsNotNone(cgroup)
        for key, val in cgroup.get_all_from('cpuset'):
            print(key, val)
        for key, val in cgroup.get_all_from('cpu'):
            print(key, val)

        cgroup.add_current_thread()
        cgroup.add_processes(*PIDS)
        # cgroup.set_value_of('cpuset', 'cgroup.procs', 28871)
        # cgroup.set_value_of('cpuset', 'cgroup.procs', 28780)
        # cgroup.add_thread(28871)

        get_from = cgroup.get_from('cpuset', 'cgroup.procs', val_type=str)
        print('last get() (cpuset):', get_from, type(get_from))

        print('TGID of test (cpuset):')
        for tgid in cgroup.get_processes_of('cpuset'):
            print(tgid)

        get_from = cgroup.get_from('cpuset', 'cgroup.procs', val_type=str)
        print('last get() (cpu):', get_from, type(get_from))

        print('TGID of test (cpu):')
        for tgid in cgroup.get_processes_of('cpu'):
            print(tgid)

        cgroup.remove_processes(*PIDS)

        print('PID of test:')
        for pid in cgroup.get_threads():
            print(pid)

        cgroup.move_to('test2')
        print(cgroup.path)
        print(cgroup.controllers)
        cgroup.delete()

    def test_existing(self):
        cgroup = CGroup.from_existing('docker')
        self.assertIsNotNone(cgroup)
        for key, val in cgroup.get_all_from('cpuset'):
            print(key, val)

        print('from all controllers:')

        for key, val in cgroup.get_all():
            if val is not None:
                print(key, val, type(val))
            else:
                print(key, 'is None')

    def test_mount_point(self) -> None:
        handler = c_void_p()
        path = create_string_buffer(4096 * 2)

        ret = cgroup_get_subsys_mount_point_begin(b'cpuset', byref(handler), path)

        while ret is 0:
            print(path.value.decode())
            ret = cgroup_get_subsys_mount_point_next(byref(handler), path)

        if ret != ErrorCode.EOF:
            _raise_error(ret)
            self.assertEqual(ErrorCode.EOF, ret)

    def test_all_controller(self) -> None:
        cgroup = CGroup('test', 'cpuset', auto_delete=True)

        controllers = tuple(cgroup.all_controller())

        for i, mp in enumerate(cgroup.all_controller()):
            print(mp)
            self.assertEqual(controllers[i], mp)


if __name__ == '__main__':
    unittest.main()
