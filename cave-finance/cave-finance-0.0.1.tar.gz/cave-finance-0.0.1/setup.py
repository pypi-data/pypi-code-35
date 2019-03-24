#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "cave-finance",
    version = "0.0.1",
    keywords = ("pip", "finance","股票","基金","爬虫"),
    description = "finance base class. 股票 基金 爬虫 基础",
    long_description = "finance base class. 股票 基金 爬虫 基础",
    license = "MIT Licence",

    url = "https://github.com/lastcaveman/finance",     
    author = "lastcaveman",
    author_email = "caveman.last@gmail.com",

    py_modules=['finance'],
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests"]
)
