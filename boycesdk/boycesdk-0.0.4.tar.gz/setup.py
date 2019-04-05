#! /usr/bin/env python
# _*_ coding:utf-8 _*_

from setuptools import setup,find_packages

setup(
    name = "boycesdk",
    version = "0.0.4",
    keyword = ("pip","boyce"),
    description = "boyce sdk",
    long_description = "boyce sdk for python",
    license = "MIT Licence",
    url = "http://www.keepstudying.club",
    author = "boyce",
    author_email = "120674007@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
    scripts = [],
    entry_points = {
        'console_scripts':[
            'boycesdk = boycesdk.help:main']
    }
)
