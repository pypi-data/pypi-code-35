from math import exp

import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            self.bit_array[result] = 1

    def lookup(self, string):
        for seed in range(self.hash_count):
            result = mmh3.hash(string, seed) % self.size
            if self.bit_array[result] == 0:
                return False
        return True


def test_bloom(m, k, n):
    # 1
    bf = BloomFilter(100000, 7)
    for i in range(5000):
        bf.add('%s' % i)

    print(bf.lookup('333'))
    print(bf.lookup('100000'))
    print(bf.lookup('500001'))
    print(bf.lookup('510001'))

    # 2
    b = BloomFilter(m, k)
    for i in range(n):
        b.add('%s' % i)
        assert b.lookup('%s' % i)

    p = (1.0 - exp(-k * (n + 0.5) / (m - 1))) ** k
    print(100.0 * p, '%')

    N = 100000
    false_pos = sum(b.lookup('%s' % i) for i in range(n, n + N))
    print(100.0 * false_pos / N, '%')


if __name__ == '__main__':
    test_bloom(1000000, 7, 100000)
