#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from bitarray import bitarray
from hashlib import md5


class EzBloom(object):

    def __init__(self, cap, fail_rate=0.001):
        """

        :param cap:       integer
        :param fail_rate: float
        """
        self.fail_rate = fail_rate
        self.bit_size = int(-(cap * math.log(fail_rate))/(math.log(2)**2))
        self.seeds_count = int((self.bit_size/cap) * math.log(2))
        self.bit_array = bitarray(self.bit_size)
        self.bit_array.setall(0)

    def add(self, val):
        m = md5()
        for seed in range(self.seeds_count):
            m.update('{}-{}'.format(val, seed).encode('utf8'))
            dig = int(m.hexdigest(), 16) % self.bit_size
            self.bit_array[dig] = True

    def is_contain(self, val):
        m = md5()
        for seed in range(self.seeds_count):
            m.update('{}-{}'.format(val, seed).encode('utf8'))
            dig = int(m.hexdigest(), 16) % self.bit_size
            if self.bit_array[dig] is False:
                return False
        return True


if __name__ == "__main__":
    cap = 100
    ef = EzBloom(cap)
    ef.add('wtf')
    assert ef.is_contain('wtf') is True
