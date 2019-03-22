#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='check_device_code',
    # 更新主函数功能   +1.0.0
    # 更新优化代码    +0.1.0
    # 更新优化说明    +0.0.1
    version='1.0.1',
    keywords='imei emid',
    packages=['check_device_code'],

    url='https://github.com/Cuile/check_device_code',
    description='校验手机设备码',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf8').read(),

    author='cuile',
    author_email='i@cuile.com'
)