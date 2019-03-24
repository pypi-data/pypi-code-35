import sys
import os
# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'z2labelmap',
      version          =   '1.1.6',
      description      =   'Convert lh/rh z-score vector to FreeSurfer labelmap', 
      long_description =   readme(),
      author           =   'Rudolph Pienaar',
      author_email     =   'rudolph.pienaar@gmail.com',
      url              =   'https://github.com/FNNDSC/pl-z2labelmap',
      packages         =   ['z2labelmap'],
      install_requires =   ['chrisapp', 'pandas', 'numpy', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['z2labelmap/z2labelmap.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
