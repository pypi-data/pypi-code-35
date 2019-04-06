#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def load_modules(path):
    dir_ = path.replace('.', '/')
    paths = []
    for filename in os.listdir(dir_):
        if filename.endswith('.py'):
            paths.append(path + '.' + filename[:-3])

    for path in paths:
        __import__(path)
