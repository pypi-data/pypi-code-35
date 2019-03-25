#!/usr/bin/env python

from distutils.core import setup
import os
import subprocess
import sys
import warnings
from os import path


__author__ = "Vcancy"
__author_email__ = "happiness1019@gmail.com"
__copyright__ = "Copyright (C) 2018 Vcancy"
__license__ = "LGPL 3.0"
__version__ = "0.0.2"

long_desc = ""
if os.path.exists("README.md") and sys.platform == "linux2":
    try:
        cmd = ['pandoc', '--from=markdown', '--to=rst', 'README.md']
        long_desc = subprocess.check_output(cmd).decode("utf8")
        print("Long DESC", long_desc)
    except Exception as e:
        warnings.warn("Exception when converting the README format: %s" % e)

setup(
    name='pycfca',
    version=__version__,
    description='Python CFCA Library',
    long_description=long_desc,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/vcancy/pycfca',
    packages=['pycfca'],
    license=__license__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "xmltodict==0.11.0",
        "lxml==4.2.3",
        "requests==2.19.1"
    ]
)
