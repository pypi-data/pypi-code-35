#!/usr/bin/env python
from setuptools import setup

setup(
    name='GregWhite',
    version='0.4.8',
    install_requires=['feedparser'],
    description='A command-line podcast aggregator',
    author='Manolo Martínez, Pepie34, Timothy White',
    author_email='tim@whiteitsolutions.com.au',
    url='https://github.com/timwhite/greg',
    packages=['greg'],
    entry_points={'console_scripts': ['greg = greg.parser:main']},
    package_data={'greg': ['data/*.conf']},
    license='GPLv3'
)
