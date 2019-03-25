#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import dirname, join

from setuptools import find_packages, setup

# Manual:
# https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html

setup(
    name="chatette_qiu",
    version="1.4.2",
    description="A dataset generator for Rasa NLU,copy from https://github.com/SimGus/Chatette,",
    author="SimGus",
    license="MIT",
    url="https://github.com/fanfanfeng/Chatette",
    packages=find_packages(),
    long_description=open(join(dirname(__file__), "README.md"),mode='r',encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Topic :: Communications",
    ],
    install_requires=[
        "enum-compat",
        "future",
    ]
)