# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(this_directory, 'VERSION'), encoding='utf-8') as f:
    version = f.read()

setup(
    name='mucho',
    version=version,
    url='https://bitbucket.org/sancorva/mucho/',
    download_url='https://bitbucket.org/sancorva/mucho/get/v{0}.zip'.format(
        version),
    license='Other/Proprietary License',
    author='Santi Cortés',
    author_email='sancorva@gmail.com',
    description='A DSL to define matching rules',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['deploy']),
    include_package_data=True,
    install_requires=[
        'lark-parser==0.6.6',
    ],
)
