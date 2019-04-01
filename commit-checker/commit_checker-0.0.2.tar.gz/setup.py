#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from __future__ import with_statement

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import commit_checker


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

requirements = []

setup_requirements = ['pytest-runner',]

test_requirements = ['pytest', 'pytest-cov', 'coverage',]

setup(
    author="Niels van der Schans",
    author_email='nvdschans@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="This is a quality tool with the goal to automate some of the reviewing work of pull requests in Bitbucket (or any other environment)",
    entry_points={
        'console_scripts': [
            'commit_checker=commit_checker.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + changelog,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='commit_checker',
    name='commit_checker',
    packages=find_packages(include=['commit_checker']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/spiked-maniac/commit_checker',
    version=commit_checker.__version__,
    zip_safe=False,
)
