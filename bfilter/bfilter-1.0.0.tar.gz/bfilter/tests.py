from __future__ import absolute_import
from bfilter.bloomfilter import BloomFilter

import unittest


class TestUnionIntersection(unittest.TestCase):
    def test_bloomFilter(self):
        bf = BloomFilter(100000, 7)
        for i in range(5000):
            bf.add('%s' % i)
        self.assertTrue(bf.lookup('42'))
        self.assertTrue(bf.lookup('5000'))
        self.assertFalse(bf.lookup('100000'))
        self.assertFalse(bf.lookup('500001'))


if __name__ == '__main__':
    unittest.main()
