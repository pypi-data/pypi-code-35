#!/usr/bin/env python

from pathlib import Path

from setuptools import find_packages, setup

README = Path(__file__).parent / 'README.md'

setup(
    name='matts-majestic-monads',
    version='0.0.2',
    description='Monadic data structures',
    long_description=README.read_text(),
    long_description_content_type='text/markdown',
    author='Matthew Franglen',
    author_email='matthew@franglen.org',
    url='https://gitlab.com/matthewfranglen/matts-majestic-monads',
    packages=find_packages(),
    install_requires=[]
)
