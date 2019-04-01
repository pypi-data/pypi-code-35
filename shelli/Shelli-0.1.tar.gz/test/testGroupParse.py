import os
import copy
import unittest

from shelli import *

defaults = host.default_options()

class TestGroupParse(unittest.TestCase):
    def setUp(self):       
        yaml = conf.YAMLoader(path='test/hostgrouptest.yml')
        self.all_hosts = host.create_hosts_from_yaml(yaml)
        self.custom_group_options = hostgroup.HostGroup(
            'custom_group_options',
            yaml['hostgroups'][0]['custom_group_options'],
            self.all_hosts
        )
        self.custom_host_options = hostgroup.HostGroup(
            'custom_host_options',
            yaml['hostgroups'][1]['custom_host_options'],
            self.all_hosts
        )
        self.custom_host_and_group_options = hostgroup.HostGroup(
            'custom_host_and_group_options',
            yaml['hostgroups'][2]['custom_host_and_group_options'],
            self.all_hosts
        )
        self.no_custom_options = hostgroup.HostGroup(
            'no_custom_options',
            yaml['hostgroups'][3]['no_custom_options'],
            self.all_hosts
        )

    def test_no_options_hash_use_defaults(self):
        self.assertEqual(self.custom_host_options.options, defaults)

    def test_hosts_type_is_dict(self):
        self.assertTrue(isinstance(self.custom_host_options.hosts, dict))
        self.assertTrue(isinstance(self.custom_group_options.hosts, dict))
        self.assertTrue(isinstance(self.custom_host_and_group_options.hosts, dict))
        
    def test_host_options_take_precedence(self):
        custom_options = copy.deepcopy(defaults)
        custom_options['auth_method'] = 'key'
        custom_options['username'] = 'test'
        custom_options['password'] = 'shhhh'
        self.assertEqual(self.custom_host_and_group_options.hosts['options_change'].options, custom_options)

    def test_host_objects_are_copied(self):
        for h in self.all_hosts:
            for h2_key in self.custom_group_options.hosts:
                self.assertTrue(h is not self.custom_group_options.hosts[h2_key])
            for h2_key in self.custom_host_options.hosts:
                self.assertTrue(h is not self.custom_host_options.hosts[h2_key])
            for h2_key in self.custom_host_and_group_options.hosts:
                self.assertTrue(h is not self.custom_host_and_group_options.hosts[h2_key])
    
    def test_shared_host_options_same(self):
        for h_key in self.no_custom_options.hosts:
            self.assertTrue(self.no_custom_options.hosts[h_key].options is self.no_custom_options.options)
    
    def test_host_options_override(self):
        for h_key in self.custom_host_options.hosts:
            self.assertTrue(self.custom_host_options.hosts[h_key].options is not self.custom_host_options.options)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
