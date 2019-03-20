#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def to_bytes(value):
    if type(value) == int:
        return int_to_bytes(value)
    elif type(value) == str:
        return str_to_bytes(value)
    elif type(value) == dict:
        return str_to_bytes(dump_dict(value))
    raise ValueError

def str_to_bytes(string):
    return bytes(string, 'utf-8')

def bytes_to_str(bytes_string):
    return bytes_string.decode('utf-8')

def bytes_to_int(bytes_string):
    return int(bytes_to_str(bytes_string))

def int_to_bytes(integer):
    integer_string = str(integer)
    zeros = 16 - len(integer_string)
    if zeros < 0:
        raise ValueError
    integer_string = f"{zeros * '0'}{integer_string}"
    return str_to_bytes(integer_string)

def dump_dict(input_dict):
    return json.dumps(input_dict, separators=(',', ':'), ensure_ascii=False)

def dump_pretty_dict(input_dict):
    return json.dumps(input_dict, indent=4, ensure_ascii=False)

def load_dict(string):
    return json.loads(string)