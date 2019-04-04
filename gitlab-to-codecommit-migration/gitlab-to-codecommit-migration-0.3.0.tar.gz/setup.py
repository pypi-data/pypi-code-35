#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import sys
import os

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

requirements = ['boto3', 'botocore', 'aws-sam-cli', 'requests']

setup_requirements = []

test_requirements = []

setup(
    author="Martin Schade",
    author_email='gitlab-to-codecommit-migration@amazon.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="The sample code provides script to migrate repositories from GitLab to AWS CodeCommit.",
    install_requires=requirements,
    scripts=['bin/gitlab-to-codecommit', 'bin/gitlab-set-read-only'],
    license="MIT-0 license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='AWS Codecommit GitLab Migration Move',
    name='gitlab-to-codecommit-migration',
    packages=['src/gitlab_codecommit_migration'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aws-samples/gitlab-to-codecommit-migration',
    version='0.3.0',
    zip_safe=False,
)
