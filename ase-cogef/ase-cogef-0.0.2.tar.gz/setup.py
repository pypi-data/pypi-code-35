#!/usr/bin/env python

# Copyright (C) 2016-2019
# See accompanying license files for details.

from __future__ import print_function
import re
import sys
from setuptools import setup, find_packages


if sys.version_info < (2, 7, 0, 'final', 0):
    raise SystemExit('Python 2.7 or later is required!')


with open('README.rst') as fd:
    long_description = fd.read()

# Get the current version number:
with open('cogef/__init__.py') as fd:
    version = re.search("__version__ = '(.*)'", fd.read()).group(1)


package_data = {'cogef': ['test/*.dat']}

setup(name='ase-cogef',
      version=version,
      description='COnstrained Geometries simulate External Force',
      url='https://wiki.fysik.dtu.dk/ase/cogef',
      maintainer='GitEdit',
      maintainer_email='oliver-bruegner@web.de',
      license='LGPLv2.1+',
      platforms=['unix'],
      packages=find_packages(),
      install_requires=['numpy', 'ase'],
      extras_require={'docs': ['sphinx', 'sphinx_rtd_theme', 'matplotlib']},
      package_data=package_data,
      entry_points={'console_scripts': ['cogef=cogef.cli.main:main']},
      long_description=long_description,
      classifiers=[
          'Development Status :: 6 - Mature',
          'License :: OSI Approved :: '
          'GNU Lesser General Public License v2 or later (LGPLv2+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Physics'])
