import os
import re
import sys
import glob
import sysconfig
import platform
import subprocess
import multiprocessing

from distutils.version import LooseVersion
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from shutil import copyfile, copymode
from setuptools import find_packages, setup, Command


setup(name='superminhash',
      version="0.1.0",
      description='A SuperMinHash implementation',
      long_description=open("README.md", "r").read(),
      long_description_content_type="text/markdown",
      url='http://github.com/fantasticfears/superminhash',
      author='nnnet',
      packages=find_packages(),
      install_requires=[
        'numpy>=1.10',
        'scikit-learn>=0.20'
      ],
      test_suite='test',
      zip_safe=False,
      classifiers=[
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
      ],
)
