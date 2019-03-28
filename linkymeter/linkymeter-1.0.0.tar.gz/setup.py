#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup



# This a function call, with many options. 
setup(

    # The name of your package, as it will appear on pypi.       
    name='linkymeter',
 
    # the version of code
    version='1.0.0',
 
    # The list of packages to be inserted in distribution
    packages=['linkymeter','linkymeter.web'],

    # Name of author
    author="ermitz",
 
    # Email
    author_email="ermitz888@gmail.com",
 
    # A short description 
    description="Get Enedis smart meter (linky) data from Enedis webserver",
 
    # A long description, will be printed to present the lib  
    # We usually dump the READ here.    
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
 
    # list of dependencies
    install_requires=['python-dateutil==2.7.5'],
 
    # An url which points to official page of lib.
    url='https://gitlab.com/ermitz/linkymeter',
 
    # It is good habits to put some metadata about the lib
    # So that bots may class it.
    # The list of possible tags is long:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Home Automation"
    ],
)

