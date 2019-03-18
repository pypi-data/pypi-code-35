#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def get_file_content(file_name):
    with open(file_name) as f:
        return f.read()

setup(
    name='qs_cs_config_parser',
    version='0.1.16',
    description='',
    author="Yoav Ekshtein, Shaul Ben Maor",
    packages=find_packages(),
    # package_data={'config_': ['data/*.yml', 'data/*.json']},
    include_package_data=True,
    install_requires=get_file_content('requirements.txt'),
    license="Apache Software License 2.0",
    # zip_safe=False,
    # keywords='shellfoundry sandbox cloud virtualization vcenter cmp cloudshell quali command-line cli',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ],
)