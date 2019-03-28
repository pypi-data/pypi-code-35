#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='IIPDarknet',
    version='0.1.0',
    description=(
        'Algorithm for object detection using YOLOv3.'
    ),
    # long_description=open('README.rst').read(),
    author='Huairui',
    author_email='wanghr827@foxmail.com',
    maintainer='Huairui',
    # maintainer_email='',
    license='BSD License',
    packages=['darknet'],
    platforms=["Linux"],
    url='http://iip.whu.edu.cn/GitLab/wangsihan/8.1Platform.git',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[

    ]
)