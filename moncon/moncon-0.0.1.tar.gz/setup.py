#!/usr/bin/env python

from setuptools import setup


setup(
    name='moncon',
    version='0.0.1',
    url='https://github.com/rcbensley/moncon/',
    description='Simple CLI wrapper for some common Monyog REST API commands.',
    packages=['moncon'],
    install_requires=['requests', ],
    scripts=['scripts/moncon', ],
    keywords='monyog',
)
