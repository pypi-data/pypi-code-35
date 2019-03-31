#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.py3',
  description = 'Aids for code sharing between python2 and python3.',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20190331',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  include_package_data = True,
  install_requires = [],
  keywords = ['python2', 'python3'],
  license = 'GNU General Public License v3 (GPLv3)',
  long_description = "Aids for code sharing between python2 and python3.\n\nPresents various names in python 3 flavour for common use in python 2 and python 3.\n\n## Function `ustr(s, e='utf-8', errors='strict')`\n\nUpgrade string to unicode: no-op for python 3.",
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  packages = ['cs.py3'],
)
