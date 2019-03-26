# coding=utf-8
# author=uliontse

# from __future__ import print_function,division
import numpy as np

def quick_sort(L):
    if len(L) > 1:
        q = L[0]
        less = quick_sort([elem for elem in L if elem < q])
        more = quick_sort([elem for elem in L if elem > q])
        return less + [q] * L.count(q) + more
    return L

_ = np.__version__
# TODO
# logging.info(算法：时间复杂度，空间复杂度)
