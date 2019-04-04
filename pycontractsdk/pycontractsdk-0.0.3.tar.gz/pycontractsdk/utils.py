#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
# Author: yuyongpeng@hotmail.com
# Description: 工具类
#  

"""

import json


def get_abi(file):
    """
    获得abi对象
    :param file:
    :return:
    """
    with open(file, 'r') as f:
        all_str = f.read()
        abi_obj = json.loads(all_str)['abi']
    return abi_obj