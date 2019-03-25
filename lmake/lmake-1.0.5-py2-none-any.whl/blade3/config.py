#!/usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = 'liuyong@agora.io(Yong Liu)'

import sys, os

current_file_dir = os.path.dirname(__file__)

build_dir = ".build"
makefile_header = current_file_dir + "/Makefile.header"

settings_list = [
    "debug",
    "release",
    "static_debug",
    "static_release",
]


def find_build_root():
    def check_path(path):
        return os.path.exists(os.path.join(path, 'BLADE_ROOT'))

    cur = os.getcwd()
    while cur != '/':
        if check_path(cur):
            return cur
        cur = os.path.split(cur)[0]
    return None

