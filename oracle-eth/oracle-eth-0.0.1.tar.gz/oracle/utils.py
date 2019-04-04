#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
工具类库
"""

import os.path
from oracle.exceptions import ValidationError
import random2
import json
import re

def create_machine_key(absfile):
    """
    生成唯一的机器标识符
    :param file: 文件的绝对路径
    :return:
    """
    if os.path.isdir(absfile):
        raise ValueError("%s must be a file", absfile)
    (path, file) = os.path.split(absfile)
    if not os.path.exists(path):
        os.makedirs(path, mode=0o777, exist_ok=False)
    with open(absfile, 'w', encoding='utf8') as f:
        rand = round(random2.SystemRandom().random() * 10000000000000000)
        f.write(str(rand))
    return rand


def get_machine_key(absfile):
    """
    获得本地的机器唯一标识符
    :param file: 文件的绝对路径
    :return: 机器标识符
    """
    if not os.path.exists(absfile):
        return create_machine_key(absfile)
    with open(absfile, 'r') as f:
        machine = f.read()
        if machine.strip().strip('\n').strip('\t') == '':
            machine = create_machine_key(absfile)
    return machine

def get_abi(abifile):
    """
    从文件中获得abi对象
    :param abifile: 本地的abi文件
    :return:
    """
    if not os.path.isfile(abifile):
        raise ValidationError("%s file is not exist" % abifile)
    with open(abifile) as f:
        json_str_data = f.read()
    json_obj = json.loads(json_str_data)
    return json_obj['abi']


def write_blocknum(cache_file, block_num):
    """
    将块号写入指定的文件
    :param cache_file:
    :param block_num:
    :return:
    """
    with open(cache_file, 'w') as f:
        f.write(str(block_num))


def get_cache_blocknum(cache_file):
    """
    获得缓存文件中的块号，如果不存在就返回0，并且新建文件
    :param cache_file:
    :return:
    """
    if os.path.isfile(cache_file):
        with open(cache_file) as f:
            block_num = f.read()
            num = block_num.strip().strip('\n').strip('\t')
            if re.match('^[0-9]+$', num):
                return int(num)
            else:
                raise ValueError('block number: %s is not number' % block_num)
    else:
        (path, file) = os.path.split(cache_file)
        if not os.path.exists(path):
            os.makedirs(path, mode=0o777, exist_ok=False)
        with open(cache_file, 'w', encoding='utf8') as f:
            f.write(str(0))
        return 0






