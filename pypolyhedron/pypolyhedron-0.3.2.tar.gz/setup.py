#!/usr/bin/env python

from setuptools import setup, Extension
import os
import numpy

cdd_dir = os.path.join('src','cddlib-094d-p1')
sources = ['cddcore.c','cddlp.c','cddmp.c','cddio.c',
           'cddlib.c','cddproj.c','setoper.c']
cdd_sources = [os.path.join(cdd_dir,'lib-src',fn) for fn in sources]
cdd_sources.append(os.path.join('src','_cddmodule.c'))
include_dirs = [os.path.join(cdd_dir,'lib-src'), numpy.get_include()]

modules=[Extension('pypolyhedron._cdd', 
                   cdd_sources, 
                   include_dirs=include_dirs)]

setup(name='pypolyhedron',
      version='0.3.2',
      description='Python interface to cdd library',
      author='Robin Deits',
      author_email='rdeits@csail.mit.edu',
      url='https://github.com/rdeits/pypolyhedron/',
      packages=['pypolyhedron'],
      package_dir={'pypolyhedron':'src'},
      install_requires=['numpy'],
      ext_modules=modules
)
