# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

PACKAGE = 'productfeeds'
VERSION = '0.5.0'

if sys.version_info < (2, 4):
    raise SystemExit("Python 2.4 or later is required  for %s %s" % (PACKAGE,
                                                                     VERSION))

setup(
    name=PACKAGE,
    version=VERSION,
    description='',
    long_description=open("README").read() + open("CHANGES").read(),
    keywords='',
    author="Maciej Czerwinski",

    author_email="maciekcz2@gmail.com",
    maintainer="Maciej Czerwinski",
    maintainer_email="maciekcz2@gmail.com",
    url='',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    package_data={'': []},
    namespace_packages=['productfeeds'],
    entry_points = {
        'console_scripts': [
            'productfeeds-import=productfeeds.command:import_feeds',
        ]
    },
    install_requires=[
        'setuptools',
        'pyyaml',
        'requests',
        'mock',
        'requests_mock',
        'MySQL-python',
        'PyXML>=0.8.4'
    ],
    zip_safe=False,
    platforms='All',
    test_suite='nose.collector',
)


