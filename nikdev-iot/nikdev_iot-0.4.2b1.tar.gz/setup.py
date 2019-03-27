# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='nikdev_iot',
      version='0.4.2b1',
      description='Python API for NikDev IoT server.',
      url='https://github.com/Niklasson-Development/nikdev_iot_python',
      author='Johan Niklasson',
      author_email='johan@nik-dev.se',
      license='MIT',
      packages=find_packages(exclude=[]),
      install_requires=[
          'requests>=2.19,<3',
      ],
      python_requires='<3',
      zip_safe=False)
