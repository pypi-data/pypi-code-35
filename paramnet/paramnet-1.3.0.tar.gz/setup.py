#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from distutils.core import setup
from itertools import chain

pkg_name = 'paramnet'
license = 'MIT'
version = '1.3.0'

extras_req = {
    'testing': ['pytest', 'pytest-pep8', 'scipy']
}

extras_req['all'] = list(chain(*extras_req.values()))

classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics"
]

with open("README.rst", "r") as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name=pkg_name.lower(),
        version=version,
        description="NetworkX graphs with required node/edge parameters",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        author="Sean P. Cornelius",
        author_email="spcornelius@gmail.com",
        url="https://github.com/spcornelius/paramnet",
        license=license,
        packages=setuptools.find_packages(),
        install_requires=['networkx>=2.0', 'numpy'],
        extras_require=extras_req,
        python_requires='>=3.6',
        classifiers=classifiers)
