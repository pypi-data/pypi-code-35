#!/usr/bin/env python
import setuptools

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'fsai_data_sdk',
    packages = setuptools.find_packages(),
    version = '1.0.3',
    description = 'The official Python fsai_data_sdk library for accessing Foresight Data Portal',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/ForesightAI/fsai_data_sdk_python',
    keywords = ['foresight', 'foresightai', 'foresightai-ai'],
    classifiers = ['Programming Language :: Python :: 2.7',
                   'License :: OSI Approved :: MIT License',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries']
)
