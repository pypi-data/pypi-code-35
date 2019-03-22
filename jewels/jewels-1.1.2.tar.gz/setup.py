#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md','r') as f:
    long_description = f.read()

setup(
    name='jewels',
    version='1.1.2',
    description='Secure file encryption and data access',
    author='andrea capitanelli',
    author_email='andrea.capitanelli@gmail.com',
    maintainer='andrea capitanelli',
    maintainer_email='andrea.capitanelli@gmail.com',
    url='https://github.com/acapitanelli/jewels',
    install_requires=[
      'pycryptodome >=3.7, <4',
    ],
    packages=['jewels'],
    package_dir={
        'jewels': 'jewels'
    },
    long_description=long_description,
    keywords='data file encryption aes256 eax cli',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography'
    ],
    scripts=[
        'bin/jewels-cli'
    ],
    test_suite='tests'
)
