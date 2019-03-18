#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['instaviz']

package_data = \
{'': ['*'], 'instaviz': ['templates/*']}

setup(name='instaviz',
      version='0.1.0',
      description='InstaViz - a tool for visulizing ASTs and CPython code objects in a web server.',
      author='Anthony Shaw',
      author_email='anthonyshaw@apache.org',
      url='https://github.com/tonybaloney/instaviz',
      packages=packages,
      package_data=package_data,
     )
