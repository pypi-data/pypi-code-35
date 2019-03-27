#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/25 13:11
# @File    : setup.py.py

import os
import re
import sys
import setuptools


def get_reqs_from_files(requirements_files):
    for requirements_file in requirements_files:
        if os.path.exists(requirements_file):
            return open(requirements_file, 'r').read().split('\n')
    return []


def parse_requirements(requirements_files=['requirements.txt']):
    requirements = []
    for line in get_reqs_from_files(requirements_files):
        # For the requirements list, we need to inject only the portion
        # after egg= so that distutils knows the package it's looking for
        # such as:
        # -e git://github.com/openstack/nova/master#egg=nova
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1',
                                line))
        # such as:
        # http://github.com/openstack/nova/zipball/master#egg=nova
        elif re.match(r'\s*https?:', line):
            requirements.append(re.sub(r'\s*https?:.*#egg=(.*)$', r'\1',
                                line))
        # -f lines are for index locations, and don't get used here
        elif re.match(r'\s*-f\s+', line):
            pass
        # argparse is part of the standard library starting with 2.7
        # adding it to the requirements list screws distro installs
        elif line == 'argparse' and sys.version_info >= (2, 7):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(requirements_files=['requirements.txt']):
    dependency_links = []
    # dependency_links inject alternate locations to find packages listed
    # in requirements
    for line in get_reqs_from_files(requirements_files):
        # skip comments and blank lines
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        # lines with -e or -f need the whole line, minus the flag
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
        # lines that are only urls can go in unmolested
        elif re.match(r'\s*https?:', line):
            dependency_links.append(line)
    return dependency_links


setuptools.setup(
    name='karl_pkg',
    version='1.0.0',
    description='karl python package sample',
    author='karl',
    author_email='karl@karl.com',

    packages=setuptools.find_packages(exclude=['bin']),
    py_modules=[],
    include_package_data=True,
    install_requires=[
        'numpy==1.13.3',
        'pandas==0.20.3',
    ],
    dependency_links=[],

    entry_points={
        'console_scripts': [
            'karl-print = karl_pkg.cmd.print_cmd:main',
        ]
    },
)
