# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 17:02:00 2019

@author: michaelek
"""

import pytest
from ecandbparams import sql_arg

##############################################
### Parameters

code = 'crc_dates'
fields = ['server', 'database', 'table']


##############################################
### Tests

def test_sql_arg_classes():
    s1 = sql_arg()
    assert len(s1.classes) >= 6


def test_sql_arg_get_dict():
    s1 = sql_arg()
    d1 = s1.get_dict(code, fields)
    assert len(d1) == 3

