#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re

from setuptools import setup, find_packages

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('cookieman/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='cookieman',
    version=version,
    url='https://gitlab.com/ergoithz/cookieman',
    license='MIT',
    author='Felipe A. Hernandez',
    author_email='ergoithz@gmail.com',
    description='Browser-aware multi-cookie flask session',
    long_description=readme,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        ],
    keywords=['web', 'browser'],
    packages=find_packages(),
    package_data={'cookieman.resources': ['*']},
    install_requires=[
        'flask',
        'werkzeug',
        'msgpack',
        'itsdangerous',
        'importlib_resources',
        'six',
        ],
    test_suite='cookieman.tests',
    tests_require=['pycodestyle'],
    zip_safe=True,
    platforms='any',
    )
