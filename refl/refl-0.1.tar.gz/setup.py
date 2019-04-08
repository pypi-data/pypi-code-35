#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='refl',
    version='0.1',
    description='Agda productivity tool',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/pypa/refl',

    # Author details
    author='Russi Chatterjee',
    author_email='root@ixaxaar.in',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Interpreters',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Haskell',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='refl, the agda tool for humans',

    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'tasks', 'scripts']),

    install_requires=['mypy', 'pytest', 'file-downloader', 'coloredlogs', 'tqdm', 'typed-ast', 'unittest2'],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    python_requires='>=3',
)
