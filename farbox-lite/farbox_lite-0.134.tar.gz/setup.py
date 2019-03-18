#/usr/bin/env python
# coding: utf8
from setuptools import setup, find_packages
from farbox_lite import version

setup(
    name='farbox_lite',
    version=version,
    description='FarBox Lite Version',
    author='Hepochen',
    author_email='hepochen@gmail.com',
    include_package_data=True,
    packages=find_packages(),
    license = 'GPL',
    install_requires = [
        'setuptools',
        'farbox_markdown',
        'pygments',
        'shortuuid',
        'unidecode',
        'python-dateutil',
        'user_agents',
        'ujson',
        'flask==0.10',
        'jinja2==2.8',

    ],

    platforms = 'linux',
)