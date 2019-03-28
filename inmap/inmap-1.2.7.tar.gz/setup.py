#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension

inmap = Extension('inmap',
                 sources = ['inmap/inmap.py', 'inmap/__init__.py', 'inmap/example.py'])

# from inmap import *

# Install : python setup.py install
# Register : python setup.py register

#  platform = 'Unix',
#  download_url = '',


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup (
    name = 'inmap',
    # version = inmap.__version__,
    version = '1.2.7',
    author = 'Aalouane Soufiane',
    author_email = 'aalouane.s@gmail.com',
    license ='gpl-3.0.txt',
    keywords="nmap, portscanner, network, pentesting",
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    platforms=[
        "Operating System :: Linux",
        ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: System :: Networking :: Monitoring",
        ],

    packages=['inmap',
              'inmap.controller',
              'inmap.core',
              'inmap.helper',
              'inmap.model',
              ],
    url = '',
    bugtrack_url = '',
    description = 'This is a python class to use nmap and access scan results from python3',
    long_description = long_description,
    long_description_content_type='text/markdown'
    )
