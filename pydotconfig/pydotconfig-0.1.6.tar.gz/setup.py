#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('./requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name="pydotconfig",
    version="0.1.6",
    description="Super simple python module for parsing structured config files with overrides",
    long_description=open('README.md').read(),
    url="https://github.com/adammhaile/dotconfig",
    license="LGPL v3.0",
    packages=['dotconfig'],
    include_package_data=True,

    install_requires=INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
    ],
    dependency_links=[]
)