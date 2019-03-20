#!/usr/bin/env python

import os

from setuptools import setup, find_packages


def get_requirements(filename: str) -> list:
    return open(os.path.join(filename)).read().splitlines()


classes = """
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]
install_requires = get_requirements('requirements.txt')
setup(
    name='epsolar-tracer',
    version='0.0.8',
    description='Tools for EPsolar Tracer A and BN solar charge controller',
    long_description=open('README.md').read(),
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    url='https://github.com/Salamek/epsolar-tracer',
    license='Apache License 2.0',
    classifiers=classifiers,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    tests_require=install_requires,
    test_suite="tests"
)
