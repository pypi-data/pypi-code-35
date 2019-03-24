#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup_requirements = [
    'pytest-runner',
    # TODO(tunnell): Put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: Put package test requirements here
]

setup(
    name='time_range',
    version='0.1.0',
    description="Methods for handling time range overlaps for scheduling, taxes, and physics applications.",
    long_description=readme + '\n\n' + history,
    author="Christopher Tunnell",
    author_email='christopher.douglas.tunnell@gmail.com',
    url='https://github.com/tunnell/time_range',
    packages=find_packages(include=['time_range']),
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='time_range',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
