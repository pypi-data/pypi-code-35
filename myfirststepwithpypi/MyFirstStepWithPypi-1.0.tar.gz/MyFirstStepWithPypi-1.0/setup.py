from setuptools import setup,find_packages,Command
import os


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

setup (

  # Fill in these to make your Egg ready for upload to
  # PyPI
  name = 'MyFirstStepWithPypi',
  version = '1.0',
  description='Some description',
  long_description='command-line tool for building/publishing/migrating consistent machine images for virtual datacenters and cloud platforms',
  packages = find_packages(),
  author = 'Joris Bremond',
  author_email = 'joris.bremond@usharesoft.com',
  license="Apache License 2.0",
  url = 'http://hammr.io',
  classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    )
)
