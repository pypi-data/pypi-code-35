import os
import copy
import unittest

from shelli import *

class TestHostParse(unittest.TestCase):
    def setUp(self):       
        self.yaml = conf.YAMLoader(path='test/targets.yml')
        self.targets = target.create_targets_from_yaml(self.yaml)
        self.abac = self.targets['abac']
        self.ab = self.targets['ab']

    def test_create_targets_type(self):
        self.assertTrue(isinstance(self.targets, dict))

    def test_all_targets_parsed(self):
        self.assertCountEqual(['abac', 'ab'], list(self.targets.keys()))

    def test_hostgroups_abac(self):
        self.assertCountEqual(['ab', 'ac'], self.abac.hostgroup_names)

    def test_transports_abac(self):
        self.assertEqual(len(self.targets['abac'].transports), 1)

    def test_commands_abac(self):
        self.assertCountEqual(self.targets['abac'].commands, ['ls /home', 'ls /test/path'])

    def test_hostgroups_ab(self):
        self.assertCountEqual(['ab'], self.ab.hostgroup_names)

    def test_transports_ab(self):
        self.assertTrue(len(self.targets['ab'].transports) == 1)

    def test_commands_ab(self):
        self.assertCountEqual(self.targets['ab'].commands, ['ls /test/path'])

    def test_get_all_hosts(self):
        hosts = self.abac.get_all_hosts()
        self.assertTrue(isinstance(hosts, dict))
        hosts2 = self.abac.get_all_hosts()
        self.assertCountEqual(hosts, hosts2)
        for one, two in zip(hosts, hosts2):
            self.assertTrue(one is two)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
