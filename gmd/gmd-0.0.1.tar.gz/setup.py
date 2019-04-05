#! /usr/bin/env python
"""A scikit-learn compatible python/cython implementation of the GMD algorithm."""

import codecs
import os

import numpy as np
from setuptools import find_packages, setup
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# get __version__ from _version.py
ver_file = os.path.join('gmd', '_version.py')
with open(ver_file) as f:
    exec(f.read())

DISTNAME = 'gmd'
DESCRIPTION = 'A scikit-learn compatible python/cython implementation of the GMD algorithm.'
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Florian Kalinke'
MAINTAINER_EMAIL = 'flops.ka@gmail.com'
URL = 'https://github.com/FlopsKa/gmd'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/FlopsKa/gmd'
VERSION = __version__
INSTALL_REQUIRES = ['numpy', 'scipy', 'scikit-learn']
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'License :: OSI Approved',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Operating System :: Unix',
               'Programming Language :: Python :: 3.7']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov',
        'pandas'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      ext_modules=[
          Extension('libgmdc',
                    sources=['gmd/libgmdc.pyx'],
                    extra_compile_args=['-O3', '-ffast-math'],
                    language='c')
      ],
      include_dirs=[np.get_include()],
      cmdclass={'build_ext': build_ext})
