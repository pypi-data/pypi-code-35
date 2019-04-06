#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='nico',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'docopt',
        'pykafka>=2.7.0'
    ],
    author='omsobliga',
    author_email='omsobliga@gmail.com',
    description='job scheduler for kafka message',
    license='MIT',
    url='https://github.com/omsobliga',
    entry_points={
        'console_scripts': [
            'nico = nico.main:main'
        ],
    }
)
