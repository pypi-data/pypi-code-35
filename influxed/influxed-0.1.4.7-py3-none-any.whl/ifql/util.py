#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
 File: util.py
 File Created: Thursday, 21st February 2019 10:17:35 pm
 Author: ESR - Romeren (emilromer@hotmail.com)
 -----
 Copyright 2019 OpenSourced, OpenSourced
 -----
 Last Modified:
 Date	By	Comments
 -----
"""

from enum import Enum

class ORDER(Enum):
    asc = 'ASC'
    desc = 'DESC'

class COMPARISON_OPERATOR(Enum):
    eq = '='
    neq = '!='
    gt = '>'
    gteq = '>='
    lt = '<'
    lteq = '<='

class INTERVAL(Enum):
    week = 'w'
    day = 'd'
    hour = 'h'
    minute = 'm'
    sec = 's'
    milisec = 'ms'
    microsec ='u'
    nanosec = 'ns'

    @property
    def factor(self):
        if(hasattr(self, '__n__')):
            return self.__n__
        return 1

    def n(self, val):
        if(isinstance(val, int) and val > 0):
            self.__n__ = val
            return self
        raise ValueError(f'Interval factor must be a positive integer, not {val}')

    def format(self):
        return f'{self.factor}{self.value}'

    def __str__(self):
        return self.format()

    @staticmethod
    def parse_interval_str(string):
        unit = INTERVAL.get_unit_from_string(string)

        val = int(string[0:len(unit)])
        return INTERVAL(unit).n(val)
    
    @staticmethod
    def get_unit_from_string(string):
        available_letters = ['w', 'd', 'h', 'm', 's', 'u', 'ns', 'ms']
        last = string[-1]

        if(last == 's' and string[-2] + last in available_letters):
                last = string[-2] + last
        
        if(last not in available_letters):
            raise ValueError(f'Interval str "{string}" is not valid')
        
        return last


class OPERATOR(Enum):
    and_= 'AND'
    or_ = 'OR'

    def __call__(self, *args):
        self.call_arguments = args
        return self

class KEY_WORDS(Enum):
    TAG_KEYS = 'TAG KEYS'
    TAG_VALUES = 'TAG VALUES'
    FIELD_KEYS = 'FIELD KEYS'
    MEASUREMENTS = 'MEASUREMENTS'
    SERIES = 'SERIES'
    DATABASES = 'DATABASES'
    RETENTION_POLICIES = 'RETENTION POLICIES'
    USERS = 'USERS'
    

class PRIVILEGES(Enum):
    READ = 'READ PRIVILEGES'
    WRITE = 'WRITE PRIVILEGES'
    ALL = 'ALL PRIVILEGES'