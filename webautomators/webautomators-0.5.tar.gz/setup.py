# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='webautomators',
      version='0.5',
      url='',
      license='MIT License (MIT)',
      author='Kaue Bonfim',
      author_email='koliveirab@indracompany.com',
      description='Application Interaction Library with Web',
      packages=['webautomators', 'test',],
      install_requires=['selenium', 'requests'],
      zip_safe=True,
      test_suite='test',
      long_description=open('README.md').read())
