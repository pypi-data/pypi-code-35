#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup
from collections import OrderedDict

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('aws_lambda_sls/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='aws-lambda-sls',
    version=version,
    url='https://github.com/dwpy/aws-lambda-sls',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/dwpy/aws-lambda-sls'),
    )),
    license='BSD',
    author='Dongwei',
    description='Python Simple Serverless for AWS Lambda Project. ',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['aws_lambda_sls'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=3.4',
    install_requires=[
        'click',
        'boto3',
        'botocore',
        'six',
        'pip>=9,<=18',
        'attrs',
        'importreqs',
        'kombu',
        'blinker'
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'sls = aws_lambda_sls.cli:main',
        ],
    },
)
