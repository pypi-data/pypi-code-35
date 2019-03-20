#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @Author:  sennhvi
# @Email:   sennhvi@gmail.com
# @Date:    3/20/19

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sbdict",
    version="0.0.1",
    author="sennhvi",
    author_email="sennhvi@gmail.com",
    description="A tool for translation from Any Language to Chinese in command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sennhvi/sbdict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)