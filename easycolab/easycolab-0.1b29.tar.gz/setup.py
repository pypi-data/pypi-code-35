#! /usr/bin/env python
#
# Copyright (C) 2019 Fernando Marcos Wittmann


# Versioning convention
# http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/specification.html
"""
The most frequent sequence-based scheme is:

MAJOR.MINOR[.MICRO]
where MAJOR designates a major revision number for the software, like 2 or 3 
for Python. Usually, raising a major revision number means that you are adding 
lot of features, breaking backward-compatibility or drastically changing the 
APIs or ABIs.

MINOR usually groups moderate changes to the software like bug fixes or minor 
improvements. Most of the time, end users can upgrade with no risks their 
software to a new minor release. In case an API changes, the end users will be 
notified with deprecation warnings. In other words, API and ABI stability is 
usually a promise between two minor releases.

Some softwares use a third level: MICRO. This level is used when the release 
cycle of minor release is quite long. In that case, micro releases are 
dedicated to bug fixes.
"""

# Difference between Alpha and Beta release
"""
Alpha Release- This is the release when the Feature which you are developing is
incomplete or partially complete. Suppose in a Ticket booking system you have 
developed the seat selection but the payment implementation is remaining. 
In this case you can release it to testers to test the initial phase of feature. Lot of Open source products do their Alpha release.

Beta Release- This release is done when the product feature is complete and all 
the development is done but there are possibilities that it could contain some 
bugs and performance issues.This release mostly done to users who test the 
product and who can report the bugs. Even UAT phase could be considered as Beta 
release.
"""

VERSION = '0.1b29'

SHORT_DESCRIPTION = "EasyColab: Easy access to the most used methods on Google Colab"

LONG_DESCRIPTION = """\
Easy to use tools to be used on Google Colab. This Python package implements some of the most useful commands such as mounting Google drive folders, download of big files and zip/unzip files.

## How to install
1. Open a Google Colab Session.
2. On a new cell, type:
```
!pip install easycolab
```
3. Try importing easycolab to check if the installation worked:
```
import easycolab as ec
```

"""

DISTNAME = 'easycolab'
AUTHOR = 'Fernando Marcos Wittmann'
AUTHOR_EMAIL = 'fernando.wittmann@gmail.com'
DOWNLOAD_URL = 'https://github.com/wittmannf/easycolab/'

try:
    from setuptools import setup
    _has_setuptools = True
except ImportError:
    from distutils.core import setup

def check_dependencies():
    install_requires = []
    return install_requires

if __name__ == "__main__":

    install_requires = check_dependencies()

    setup(
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            "Programming Language :: Python :: 2",
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
        description=SHORT_DESCRIPTION,
        install_requires=install_requires,
        license="MIT",
        long_description=LONG_DESCRIPTION,
        include_package_data=True,
        keywords='easycolab',
        name='easycolab',
        packages=['easycolab'],
        url=DOWNLOAD_URL,
        version=VERSION,
        zip_safe=False,
    )
