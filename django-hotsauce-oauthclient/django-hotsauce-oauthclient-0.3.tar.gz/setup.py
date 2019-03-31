#!/usr/bin/env python
from __future__ import with_statement

import sys, os, posixpath
workdir = os.getcwd()
# adds 'lib' to sys.path 
sys.path.insert(0, posixpath.join(workdir, 'lib'))

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import distutils.cmd
import tempfile
import shutil
import wsgi_oauth2

try:
    with open('README.rst') as fd:
        long_description = fd.read()
except IOError:
    long_description = None


setup(name='django-hotsauce-oauthclient',
      description='Simple WSGI middleware for OAuth 2.0',
      long_description=long_description,
      version=wsgi_oauth2.__version__,
      maintainer="Etienne Robillard",
      author_email="tkadm30@yandex.com",
      license='Apache',
      # Include stuff which belong in SVN or mentioned in MANIFEST.in
      include_package_data=True,
      package_dir={'': 'lib'},
      packages=find_packages(where='lib'),
      classifiers=[
          #'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          #'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware'
      ],
      #cmdclass=cmdclass
      )
