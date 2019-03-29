#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


with open("requirements.in") as f:
    INSTALL_REQUIRES = f.read().splitlines()


setup(
    name="pytest-diff",
    version="0.1.8",
    author="User Name",
    author_email="email@example.com",
    maintainer="User Name",
    maintainer_email="email@example.com",
    license="MIT",
    url="https://github.com/username/pytest-diff",
    description="A simple plugin to use with pytest",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    py_modules=["pytest_diff"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["diff = pytest_diff"]},
)
