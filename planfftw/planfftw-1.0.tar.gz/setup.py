#!usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from glob import glob
from os.path import splitext, basename

with open("README.md") as fh:
    long_description = fh.read()

__version__ = "1.0"


setup(name="planfftw",
      version=__version__,
      license="GPL-3.0",
      description="Julia-inspired function planners around pyfftw",
      long_description=long_description,
      author="Stefan Peterson",
      author_email="stefan.peterson@rubico.com",
      url="https://github.com/sjpet/planfftw",
      packages=find_packages("src"),
      package_dir={"": "src"},
      py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
      include_package_data=True,
      download_url="https://github.com/sjpet/planfftw/tarball/%s" % __version__,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities'],
      install_requires=["numpy"],
      extras_require={"speed": ["pyfftw"],
                      "dev": ["pytest", "tox", "scipy", "pyfftw"]},
      tests_require=["pytest"],
      keywords=["pyfftw", "fft", "fftw", "plan", "planner"])

