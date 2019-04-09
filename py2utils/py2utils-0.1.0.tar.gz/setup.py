#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: kai.zhang1@nio.com
Last modified: 2019-04-07 00:07:43
'''
from setuptools import setup


setup(
    name="py2utils",
    version="0.1.0",
    description="digua python utils",
    author="zhangkai",
    author_email="zkdfbb@qq.com",
    url="http://www.ishield.cn",
    license="MIT",
    python_requires='>=3.6',
    install_requires=['tornado', 'numpy'],
    include_package_data=True,
    py_modules=[
        'utils',
    ],
    classifiers=[
        # 发展时期
        'Development Status :: 4 - Beta',
        # 开发的目标用户
        'Intended Audience :: Developers',
        # 属于什么类型
        'Topic :: Software Development :: Build Tools',
        # 许可证信息
        'License :: OSI Approved :: MIT License',
        # 目标 Python 版本
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
