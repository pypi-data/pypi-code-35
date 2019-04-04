#!/usr/bin/env python

from setuptools import setup

setup(name='no-headers-target-csv',
      version='0.0.5',
      description='Singer.io target for writing CSV files with or without headers.',
      author='Stitch',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['no-headers-target-csv'],
      install_requires=[
          'jsonschema==2.6.0',
          'singer-python==2.1.4',
      ],
      entry_points='''
          [console_scripts]
          no-headers-target-csv=no_headers_target_csv.no_headers_target_csv:main
      ''',
)
