"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-kdl-ldap',

    version='1.2',

    description='Django LDAP authentication for KDL',
    long_description=long_description,

    url='https://github.com/kingsdigitallab/django-kdl-ldap',

    author='King\'s Digital Lab',
    author_email='kdl-info@kcl.ac.uk',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP',
        'Topic :: Utilities',
    ],

    keywords='django kdl ldap',

    packages=['kdl_ldap'],

    include_package_data=True,

    install_requires=['django-auth-ldap'],
)
