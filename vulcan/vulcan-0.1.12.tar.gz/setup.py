#!/usr/bin/env python

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

from os import path
import os

this_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(this_directory, 'README.md')
if os.path.exists(readme_path):
    with open(readme_path) as f:
        long_description = f.read()
else:
    long_description = ""

setup(name='vulcan',
      version='0.1.12',
      description='Terminal-based flashcard application, for developers, that uses machine learning to schedule reviews',
      author='Shyal',
      author_email='shyal@shyal.com',
      url='https://www.github.com/shyal/vulcan/',
      packages=['vulcan', 'vulcan.lib', 'vulcan.vulcan_db', 'vulcan.vulcan_db.versions'],
      scripts=['vulcan/vulcan'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      install_requires=[
      'urwid',
      'pygments',
      'sqlalchemy',
      'arrow',
      'sqlalchemy-migrate',
      ])

