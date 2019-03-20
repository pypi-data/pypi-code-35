
# -*- coding: utf-8 -*-
"""
Ginga Client
-------------
A Distributed Lock Client
"""
from distutils.core import setup

setup(
    name='ginga-client',
    version='1.0.1',
    description='A Distributed Lock Client',
    author='Monomer Xu',
    author_email='fing@easymail.com.cn',
    url='https://github.com/FastSchnell/Ginga-Client-Py',
    py_modules=['gcp'],
    packages=['gcp'],
    license='Apache License, Version 2.0',
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
