#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

from setuptools import setup, find_packages
print(find_packages())
setup(
    name = "pyidrac",
    version = "0.1.1",
    keywords = ("pip", "pyidrac"),
    description = "pyidrac physical mechine info",
    long_description = "pyidrac physical mechine info",
    license = "MIT Licence",
    url = "https://github.com/zhangliu520/pyidrac.git",
    author = "zl",
    author_email = "752477168@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],

)

