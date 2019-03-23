#!/usr/bin/env python

import os.path
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


setup(
    name='django-schemahybrid-translation',
    version='0.1.3',
    find_packages=find_packages(),
    include_package_data=True,
    license='WTFPL',
    description='Translations stored as a JSONField (postgres only)',
    long_description=README,
    author='Unicstay',
    author_email='dev@unicstay.com',
    install_requires=[
        'Django>=1.9',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
