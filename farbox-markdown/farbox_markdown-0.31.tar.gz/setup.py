#/usr/bin/env python
# coding: utf8
from setuptools import setup, find_packages
from farbox_markdown import version

setup(
    name='farbox_markdown',
    version=version,
    description='Markdown Compiler for FarBox',
    author='Hepochen',
    author_email='hepochen@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    license = 'GPL and not allowed for commercial use',
    install_requires = [
        'pygments',
        'shortuuid',
        'PyYAML==3.11',
        'pyaml==13.12.0'
        #'bs4==4.4.1'
    ],

    platforms = 'linux',
)