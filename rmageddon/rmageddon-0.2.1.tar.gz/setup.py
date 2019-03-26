#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

version = '0.2.1'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='rmageddon',
    version=version,
    description='Small linting and building tool for R containers at QBiC',
    long_description=readme,
    keywords=['R', 'linting', 'lint', 'Docker', 'container'],
    author='Sven Fillinger',
    author_email='sven.fillinger@qbic.uni-tuebingen.de',
    license=license,
    scripts=['scripts/rmageddon'],
    install_requires=required,
    setup_requires=[
                       'twine>=1.11.0',
                       'setuptools>=38.6.',
                   ] + ([] if sys.version_info.minor == 4 else ['wheel>=0.31.0']),
    packages=find_packages(exclude='docs'),
    include_package_data=True
)
