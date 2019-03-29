#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('yatom/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='yatom',
    version=version,
    url='https://gitlab.com/ergoithz/yatom',
    license='MIT',
    author='Felipe A. Hernandez',
    author_email='ergoithz@gmail.com',
    description='Beautiful HTML/XHTML/XML using YAML',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        ],
    keywords=['yaml', 'html'],
    packages=find_packages(),
    package_data={'yatom.tests.resources': ['*']},
    install_requires=['pyyaml', 'six'],
    test_suite='yatom.tests',
    tests_require=['pycodestyle', 'importlib_resources'],
    zip_safe=True,
    platforms='any',
    )
