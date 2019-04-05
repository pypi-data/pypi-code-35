from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import math


class CounterDictionary:

    def __init__(self):
        self._table = {}


    def putlist(self, lst):
        for i in lst:
            self[i] = 1

    def __getitem__(self, key):
        return self._table[key]


    def __setitem__(self, key, value):
        if key not in self._table:
            self._table[key] = 0
        self._table[key] += value


    def __delitem__(self, key):
        del self._table[key]


    def clear(self):
        self.table = {}


    def sum(self, *keys):
        if not keys:
            keys = self._table.keys()

        ret = 0
        for key in keys:
            ret += self._table[key]
        return ret


    def keys(self):
        return self._table.keys()


    def values(self):
        return self._table.values()


    def items(self):
        return self._table.items()


    def max(self):
        m = 0
        mk = None
        for k, v in self._table.items():
            if v > m:
                m = v
                mk = k
        return (mk, m)


    def min(self):
        first = True
        m = 0
        mk = None
        for k, v in self._table.items():
            if first:
                first = False
                m = v
                mk = k
            elif v < m:
                m = v
                mk = k
        return (mk, m)

    
    def _square(self, x):
        return x * x

    
    def _sum(self, vals):
        ret = 0
        for val in vals:
            ret += val
        return ret


    def stdev(self):
        vals = list(self.values())
        avg = self.sum() / len(vals)
        return math.sqrt(self._sum([self._square(x - avg) for x in vals]) / len(vals))


    def __str__(self):
        lst = []
        for k,v in self._table.items():
            lst.append('{}: {}'.format(k, v))
        if not lst:
            return '(Empty)'

        return ', '.join(lst)
