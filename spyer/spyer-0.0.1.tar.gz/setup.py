#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='spyer',
    version='0.0.1',
    author='ce',
    author_email='zbing3@163.com',
    url='https://opslinux.com',
    description=' 麻瓜编程',
    packages=['spyer'],
    install_requires=[
        'lxml==4.3.1',
        'beautifulsoup4==4.7.1',
        'requests==2.21.0',
        'redis==3.1.0',
        'selenium==3.141.0',
        'w3lib==1.20.',
    ],
)