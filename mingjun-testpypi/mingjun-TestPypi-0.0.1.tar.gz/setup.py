#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='mingjun-TestPypi',
    version='0.0.1',
    author='anly.pear',
    author_email='anly.pear@gmail.com',
    description=u'测试',
    url='https://github.com/mingjunli',
    packages=['main'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'hello=main:hello',
            'hau=main:hau'
        ]
    }
)