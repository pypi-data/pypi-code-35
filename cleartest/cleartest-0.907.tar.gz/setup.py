#!/usr/bin/env python
 
from setuptools import setup

setup(name='cleartest',
    version='0.907',
    description='Lightweight testing framework for Python 3.7 & above and Python 2.7',
    long_description="See the project's GitHub page for docs: https://github.com/sbarba/cleartest",
    py_modules=['cleartest'],
    author='Steve Barba',
    license='MIT',
    scripts=['runtests'],
    url='https://github.com/sbarba/cleartest',
    install_requires=[
        'glob2',
        'colorama',
        'requests'
    ],
)
