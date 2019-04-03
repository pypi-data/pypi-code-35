# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from setuptools import setup, Extension

with open('readme.md', 'r') as f:
  long_description = f.read()

extension = Extension(
  'hashing.cpython',
  sources=['hashing/cpython.cpp'],
  extra_compile_args=['-std=c++11', '-maes', '-Wall'],
  include_dirs=[])

setup(
  long_description=long_description,
  ext_modules=[extension])
