import os

from setuptools import setup

from pysqlitequeue import __version__

PACKAGE_NAME = 'PySqliteQueue'
DESCRIPTION = 'Sqlite based queue'
with open(os.path.join(os.path.dirname(__file__),
                       'README.rst')) as f:
    LONG_DESCRIPTION = f.read()
DOWNLOAD_URL = 'https://pypi.org/project/PySqliteQueue/#files'
MAINTAINER = 'Mark Andreev'
MAINTAINER_EMAIL = 'mark.andreev@gmail.com'
LICENSE = 'MIT License'


def setup_package():
    setup(name=PACKAGE_NAME,
          version=__version__,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          author=MAINTAINER,
          author_email=MAINTAINER_EMAIL,
          download_url=DOWNLOAD_URL,
          license=LICENSE,
          platforms='any',
          packages=['pysqlitequeue'],
          classifiers=[
              'License :: OSI Approved :: MIT License',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3.6',
              'Topic :: Software Development :: Libraries :: Python Modules',
          ])


if __name__ == "__main__":
    setup_package()
