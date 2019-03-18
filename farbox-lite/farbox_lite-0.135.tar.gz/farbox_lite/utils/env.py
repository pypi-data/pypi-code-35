#coding: utf8
from __future__ import absolute_import
import os


def get_env(key):
    lower_key = key.lower()
    v = os.environ.get(key) or os.environ.get(lower_key)
    if v:
        return v
    filenames  = [key, '%s.txt'%key]
    if lower_key not in filenames:
        filenames += [lower_key, '%s.txt'%lower_key]
    for filename in filenames:
        filepath = os.path.join('/tmp/env', filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                raw_content = f.read()
            v = raw_content.strip()
            if v:
                return v




