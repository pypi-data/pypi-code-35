#!/usr/bin/env python
# coding=utf8 
from setuptools import setup, find_packages

setup(
    name         = 'pyspiderman',
    version      = '0.7.a1',
    description=(
        'scrapy project integrated with useful utils,focus on programing your spider logic.'
    ),
    long_description=open('README.rst').read(),
    author='vikky',
    author_email='1309550760@qq.com',
    maintainer='vikky',
    maintainer_email='1309550760@qq.com',
    license='Apache License 2.0',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vikky-lin/spiderman',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
