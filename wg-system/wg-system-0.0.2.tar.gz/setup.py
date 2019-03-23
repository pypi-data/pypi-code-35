#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup

def get_version(package):
    """
    Return package version as listed in `__version__` in `__version__.py`.
    """
    with open(os.path.join(package, "__version__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)

def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


setup(
    name="wg-system",
    python_requires=">=3.6",
    version=get_version("wg_system"),
    url="https://gitlab.com/hashdivision/wgsystem",
    license="Apache License 2.0",
    description="Worldman Games System",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Igor Nehoroshev",
    author_email="mail@neigor.me",
    packages=get_packages("wg_system"),
    data_files=[("", ["LICENSE"])],
    include_package_data=True,
    install_requires=[
        "starlette",
        "databases[postgresql]"
    ],
    extras_require={
        "registration": [
            "python-multipart", # for getting form data from request
            "aiosmtplib", # for sending emails
            "requests-async" # for ReCAPTCHA checks
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)