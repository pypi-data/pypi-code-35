# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gemeinsprache',
    version='0.1.0',
    description='General purpose utility functions and class objects required by other python projects',
    long_description=readme,
    author='Kevin Zeidler',
    author_email='kzeidler@gmail.com',
    url='https://github.com/ProbonoBonobo/gemeinsprache',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
