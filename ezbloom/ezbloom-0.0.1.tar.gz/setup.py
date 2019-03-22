#!/usr/bin/env python
# coding=utf-8
from setuptools import setup

# This call to setup() does all the work
setup(
    name="ezbloom",
    version="0.0.1",
    description="Easy bloom filter",
    url="https://github.com/watermelo/ezbloom",
    author="melo",
    author_email="watermelo@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["ezbloom"],
    include_package_data=True,
    install_requires=["bitarray"],
)
