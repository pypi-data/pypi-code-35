# -*- coding: utf-8 -*-
# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages
from io import open 

with open('README.md', "r", encoding='utf-8') as f:
    __readme__ = f.read()

with open('LICENSE') as f:
    __license__ = f.read()

__version__ = "0.1.rc1"

setup(
    name='anisocado',
    version=__version__,
    description='Generate off-axis SCAO PSFs for MICADO at the ELT',
     author='Eric Gendron, Kieran Leschinski',
    author_email='kieran.leschinski@univie.ac.at',
    url='https://github.com/astronomyk/anisocado',
    license="GNU GENERAL PUBLIC LICENSE Version 2, June 1991",
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['numpy', 'astropy', 'matplotlib'],
    long_description=__readme__,
    long_description_content_type = 'text/markdown'
   )
