# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:49:17 2019

@author: nov28
"""


import sys
import os
import collections
class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = collections.OrderedDict()
        

    def get(self, key: int):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return False


    def put(self, key: int):
        try:
            self.cache.pop(key)
        except KeyError:    
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = key
        
    def contents(self):
        return self.cache

def main():
    
    l= LRUCache()
    
    


if __name__=="__main__":
    main()
    