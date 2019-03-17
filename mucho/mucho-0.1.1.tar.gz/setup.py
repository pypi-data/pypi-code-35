# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='mucho',
    version='0.1.1',
    url='https://bitbucket.org/sancorva/mucho/',
    download_url='https://bitbucket.org/sancorva/mucho/get/v0.1.1.zip',
    license='Other/Proprietary License',
    author='Santi Cortés',
    author_email='sancorva@gmail.com',
    description='A DSL to define matching rules',
    packages=find_packages(exclude=['deploy']),
    include_package_data=True,
    install_requires=[
        'lark-parser==0.6.6',
    ],
)
