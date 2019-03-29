#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='mobi-parse',
    version='1.0.1',
    description=(
        'mobi parse'
    ),
    long_description=open('README.rst').read(),
    author='eric_zyh',
    author_email='8040334@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/ericzyh/mobi-parse',
    install_requires=[
        'bitarray==0.8.1'
    ],
    classifiers=[
    ],
)
