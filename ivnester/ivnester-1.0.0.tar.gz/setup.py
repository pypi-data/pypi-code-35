# from distutils.core import setuppyt
from setuptools import setup, find_packages

setup(
    name         = 'ivnester',
    version      = '1.0.0',
    license      = 'MIT License',
    install_requires = [],
    include_package_data = True,
    packages     = ['ivnester'],
    author       = 'ivnstar',
    author_email = '44828299@qq.com',
    url          = 'http://www.ivnature.cn',
    description  = 'A simple printer of nested lists',
)