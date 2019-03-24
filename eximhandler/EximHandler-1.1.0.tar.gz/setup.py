#!/usr/bin/env python
# encoding=utf8

import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='EximHandler',
    version='1.1.0',
    author='Dan Michael O. Heggø',
    author_email='danmichaelo@gmail.com',
    description='A logging handler class which sends an email using exim',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/danmichaelo/eximhandler',
    packages=['eximhandler'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
