# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='nikdev_iot',
      version='0.5.1rc1',
      description='Python API for NikDev IoT server.',
      long_description=long_description,
      url='https://github.com/Niklasson-Development/nikdev_iot_python',
      author='Johan Niklasson',
      author_email='johan@nik-dev.se',
      license='MIT',
      packages=find_packages(exclude=[]),
      install_requires=[
          'requests>=2.19,<3',
      ],
      python_requires='>=2.7, <4',
      zip_safe=False)
