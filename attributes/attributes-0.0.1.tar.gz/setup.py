# -*- coding: utf-8 -*-
#
# Copyright (c) 2019~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from setuptools import setup, find_packages

long_description = ''

if os.path.isfile('README.md'):
    with open('README.md') as fp:
        long_description = fp.read()

long_description = long_description or ''

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    name='attributes',
    version='0.0.1',
    description='',
    keywords=[],
    author='Cologler',
    author_email='skyoflw@gmail.com',
    url='https://github.com/Cologler/attributes-python',
    license='MIT License',
    classifiers=[],
    scripts=[],
    entry_points={},
    zip_safe=False,
    include_package_data=True,
    setup_requires=[],
    install_requires=[],
    tests_require=[],
)
