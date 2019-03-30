# -*- coding:utf-8 -*-
import os
import base64
import hashlib
import sys
import json

# upload  resnet
def filter_id(data_list):
    for d in data_list:
        del d['_id']
    return data_list

# upload resnet
def get_md5(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()

# upload resnet
def get_suffix(filename):
    segs = os.path.split(filename)
    return os.path.splitext(segs[1])[1]

# upload resnet
def transcode(data):
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = transcode(v)

    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = transcode(data[i])

    elif isinstance(data, unicode):
        data = data.encode('utf-8')
    return data

# upload resnet
def encode_name(name):
    seg = name.split('-')
    seg[1] = base64.b64encode(seg[1])
    name = seg[0] + '-' + seg[1]
    return name

# upload resnet
def decode_name(name):
    seg = name.split('-')
    seg[1] = base64.b64decode(seg[1])
    name = seg[0] + '-' + seg[1]
    return name

# resnet
def get_magicNum(src):
    md5 = get_md5(src)
    md5 = int(md5, 16)
    magic_num = md5 % 10
    return magic_num

def main():
    print get_suffix('a/a.bb')
    print get_suffix('a.bb')
    print get_suffix('abb')


if __name__ == '__main__':
    main()
