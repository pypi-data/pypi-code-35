#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "python-bitcoinrpc", "requests" ]

setup_requirements = [ ]

test_requirements = [ "python-bitcoinrpc", "requests" ]

setup(
    author="Aleksandar Nikolaev Dinkov",
    author_email='alexander.n.dinkov@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A collection of wallet modules for PipeCaead http://pipe.cash/ for more information.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pipecashwallets',
    name='pipecashwallets',
    packages=find_packages(include=['pipecashwallets']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Pipe-Cash/pipecashwallets',
    version='0.1.2.0',
    zip_safe=False,
)
