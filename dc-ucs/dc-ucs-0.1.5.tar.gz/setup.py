#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : setup.py.py
@Author: donggangcj
@Date  : 2019/4/1
@Desc  : 
'''

from setuptools import setup  # 这个包没有的可以pip一下

setup(
    name="dc-ucs",  # 这里是pip项目发布的名称
    version="0.1.5",  # 版本号，数值大的会优先被pip
    keywords=["pip", "UCS", "COMMAND LINE"],
    description="UCS user clean tool",
    long_description="The tool is aimed to clean the dirty data when develop and test the ucs portal project",
    license="MIT Licence",

    url="https://github.com/donggangcj/ucs.git",  # 项目相关文件地址，一般是github
    author="GangDong",
    author_email="donggangcj@gmail.com",

    # packages=find_packages(),
    packages=['ucs'],
    include_package_data=True,
    platforms="any",
    install_requires=[
        "requests",
        "Click",
        "PyMySQL",
        "SQLAlchemy"
    ],  # 这个项目需要的第三方库
    entry_points={
        'console_scripts': [
            'dc-ucs=ucs.ucsclean:clean_dce']
    }
)
