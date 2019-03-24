#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:  setup .py
Author: Lijiacai (1050518702@qq.com)
Date: 2018-11-22
Description:
    setup tool
"""

import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)

from setuptools import setup
from setuptools import find_packages

setup(
    name="SpiderTool",
    version="19.03.24",
    keywords=("pip", "SpiderTool", "spider", "spidertool"),
    description="The package for Spider",
    long_description="Packing provides two types of crawlers, Browser and Request, " +
                     "which can extend or retain the necessary crawler methods, " +
                     "avoid configuration methods and improve grasping efficiency.",
    license="",

    url="https://github.com/lijiacaigit/SpiderTool",
    author="Lijiacai",
    author_email="1050518702@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "selenium"]  # 这个项目需要的第三方库
)
