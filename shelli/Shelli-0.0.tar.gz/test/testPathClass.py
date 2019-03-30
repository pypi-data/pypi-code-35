import os
import unittest

from shelli import *

class TestPackageOptions(unittest.TestCase):
    def setUp(self):       
        yaml = conf.YAMLoader(path='test/simple.yml')
        self.hosts = host.createHostsFromYaml(yaml)

    def test_options_hash(self):
        for h in self.hosts:
            if h.hostname == 'ns3':
                self.assertEqual(h.hostname, 'ns3')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
