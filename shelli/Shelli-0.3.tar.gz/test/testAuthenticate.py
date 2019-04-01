import os
import copy
import unittest
from unittest.mock import patch

from shelli import *

defaults = host.default_options()

class TestAuthenticate(unittest.TestCase):
    def setUp(self):
        self.options = host.default_options()
        self.options.update({'password':''})
        self.host = host.Host('fiat', self.options)
        self.conn = authenticate.get_connection(self.host)
        pass

    def test_get_connection(self):
        options = host.default_options()
        options.update({'password':''})
        conn = authenticate.get_connection(host.Host('fiat', options))
        self.assertEqual(conn.host, 'fiat')
        self.assertEqual(conn.port, 22)

    def test_reuse_connections(self):
        before_id = id(self.host)
        conn = authenticate.get_connection(self.host)
        conn = authenticate.get_connection(self.host)
        conn = authenticate.get_connection(self.host)
        conn = authenticate.get_connection(self.host)
        
        self.assertEqual(list(authenticate.CONNECTION_DICT.keys())[0], before_id)
        self.assertEqual(len(authenticate.CONNECTION_DICT.keys()), 1)

    def tearDown(self):
        authenticate.CONNECTION_DICT = {}
        pass

if __name__ == '__main__':
    unittest.main()
