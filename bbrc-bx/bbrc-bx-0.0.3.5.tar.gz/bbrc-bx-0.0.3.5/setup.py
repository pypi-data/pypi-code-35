import setuptools
from setuptools import setup

import os.path as op
this_directory = op.abspath(op.dirname(__file__))
with open(op.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
  name = 'bbrc-bx',
  install_requires=requirements,
  scripts=['bin/bx'],
  long_description=long_description,
  long_description_content_type='text/markdown',
  version = '0.0.3.5',
  description = 'BarcelonaBeta + XNAT = bx',
  packages=setuptools.find_packages(),
  author = 'Greg Operto',
  author_email = 'goperto@barcelonabeta.org',
  url = 'https://gitlab.com/xgrg/bx',
  download_url = 'https://gitlab.com/xgrg/bx/-/archive/v0.0.3.5/bx-v0.0.3.5.tar.gz',
  classifiers = ['Intended Audience :: Science/Research',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering',
      'Operating System :: Unix',
      'Programming Language :: Python :: 3.7' ]
)
