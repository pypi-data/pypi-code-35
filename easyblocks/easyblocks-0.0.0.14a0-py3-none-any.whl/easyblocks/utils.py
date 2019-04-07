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
    elif type(value) == bool:
        if value:
            return int_to_bytes(1)
        return int_to_bytes(0)
    raise ValueError(type(value))

def str_to_bytes(string):
    if string == None:
        return
    return bytes(string, 'utf-8')

def bytes_to_str(bytes_string):
    if bytes_string == None:
        return
    return bytes_string.decode('utf-8')

def bytes_to_int(bytes_string):
    if bytes_string == None:
        return
    return int(bytes_to_str(bytes_string))

def bytes_to_dict(bytes_dict):
    str_dict = bytes_to_str(bytes_dict)
    if str_dict == None:
        return
    return load_dict(str_dict)

def get_padded_int(integer):
    integer_string = str(integer)
    zeros = 16 - len(integer_string)
    if zeros < 0:
        raise ValueError
    integer_string = f"{zeros * '0'}{integer_string}"
    return integer_string

def int_to_bytes(integer):
    return str_to_bytes(get_padded_int(integer))

def dump_dict(input_dict):
    return json.dumps(input_dict, separators=(',', ':'), ensure_ascii=False)

def dump_pretty_dict(input_dict):
    return json.dumps(input_dict, indent=4, ensure_ascii=False)

def load_dict(string):
    return json.loads(string)