#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    File Name: setup.py
    Author: HuHao
    Mail: whohow20094702@163.com
    Created Time:  '2019/2/28 20:48:00'
    Info: A effective style to operate sql
          Support for HA-connection, retry-support, high-tolerance params, self-batch execution
    Licence: GPL Licence
    Url: https://github.com/GitHuHao/effective_sql.git

"""

from setuptools import setup, find_packages

setup(
    name="effective",
    version="0.1.24",
    keywords=("pip", "upsert","crud", "mysql", "sql", "logging"),
    description="A effective style to play in python",
    long_description='''effective.sql:
                            Support for HA-connection, retry-support, high-tolerance params, self-batch execution
                        effective.logger:
                            multiprocess logging
                     ''',
    license="GPL Licence",
    url="https://github.com/GitHuHao/effective.git",
    author="HuHao",
    author_email="whohow20094702@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['pymysql', 'DBUtils', 'gevent', 'errno', 'logging']
)

