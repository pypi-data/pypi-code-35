#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

# version
here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here, 'daisy', '__init__.py'))
                if line.startswith('__version__ = ')),
               '0.0.dev0')

install_requires=[
        'luigi>=2.8.2'
        ]


setup(
    name="luigi-daisy",
    version=version,
    url='https://github.com/nunukim/daisy',
    author='Ryota Suzuki',
    author_email='ryouta_suzuki@yahoo.co.jp',
    maintainer='Ryota Suzuki',
    maintainer_email='ryouta_suzuki@yahoo.co.jp',
    description='Utility wrapper of luigi',
    long_description=readme,
    packages=find_packages(),
    install_requires=install_requires,
    license="BSD",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
    """,
)
