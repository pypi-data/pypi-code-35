#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='noseprogress',
    version='0.7',
    description=(
        'A nosetests plugin with progress before testcase'
    ),
    long_description=open('README.md').read(),
    author='land',
    author_email='landhu@hotmail.com',
    maintainer='land',
    maintainer_email='landhu@hotmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/landhu/nose-progress',
    entry_points = {
        'nose.plugins': [
            'nosescheduling = noseprogress.noseprogress:Progress'
            ]
        },
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
