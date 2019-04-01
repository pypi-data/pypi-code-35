#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='get-time',
    version='0.0.4',
    author='黄民航',
    author_email='gmhesat@gmail.com',
    url='https://github.com/Coxhuang/get_time',
    description='获取任意时间/获取当前的时间戳/时间转时间戳/时间戳转时间',
    packages=['get_time'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get_time=get_time:get_time',
            'get_timestamp=get_time:get_timestamp',
            'timestamp_to_str=get_time:timestamp_to_str',
            'str_to_timestamp=get_time:str_to_timestamp',
        ]
    }
)

