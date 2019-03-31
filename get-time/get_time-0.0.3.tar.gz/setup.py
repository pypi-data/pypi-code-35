#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='get_time',
    version='0.0.3',
    author='黄民航',
    author_email='gmhesat@gmail.com',
    url='https://github.com/Coxhuang/get_time',
    description='获取任意时间',
    packages=['get_time'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get_time=get_time:get_time'
        ]
    }
)

