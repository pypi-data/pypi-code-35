# -*- coding: utf-8 -*-
# Author: ZhangTianJie

import setuptools

try:
    long_description = open('README.md', encoding='utf8').read()
except:
    long_description = 'python configuration file loading package',

setuptools.setup(
    name='py_configfile',
    version='0.0.4',
    description='python configuration file loading package',
    long_description=long_description,
    long_description_content_type="text/markdown",

    py_modules=["configfile"],

    url='http://github.com/ztj1993/py_configfile',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',

    keywords='configfile config json yaml',
    install_requires=['pyyaml'],

    license='MIT',
)
