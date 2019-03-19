#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: LiangjunFeng
# Mail: zhumavip@163.com
# Created Time:  2018-4-16 19:17:34
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "ttTest",      #这里是pip项目发布的名称
    version = "1.0.1",  #版本号，数值大的会优先被pip
    keywords = ["pip", "ttTest"],
    description = "a test project",
    long_description = "a test project long",
    license = "SHL Licence",

    url = "https://github.com/songhanlu/game/projects/1",     #项目相关文件地址，一般是github
    author = "Songhanlu",
    author_email = "13621083224@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy"]          #这个项目需要的第三方库
)