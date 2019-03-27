import unittest
from ybc_funny import *


class MyTestCase(unittest.TestCase):
    def test_jizhuanwan(self):
        self.assertIsNotNone(jizhuanwan_content())

    def test_raokouling(self):
        self.assertIsNotNone(raokouling())

    def test_xiehouyu(self):
        self.assertIsNotNone(xiehouyu_content())

    def test_miyu(self):
        self.assertIsNotNone(miyu_content())

    def test_xiaohua(self):
        self.assertIsNotNone(xiaohua())


if __name__ == '__main__':
    unittest.main()
