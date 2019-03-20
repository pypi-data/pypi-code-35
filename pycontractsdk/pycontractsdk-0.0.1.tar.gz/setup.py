#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="pycontractsdk",
    version="0.0.1",
    author="yuyongpeng",
    author_email="yuyongpeng@hotmail.com",
    description=("This is a sdk of constract"),
    long_description_markdown_filename='README.md',
    license="MIT",
    keywords="solidity web3 constract sdk",
    url="https://gitlab.hard-chain.cn/cport/pyconstractsdk",
    # packages=['pycontractsdk'],  # 需要打包的目录列表
    packages = find_packages(where='.', exclude=('tests', 'tests.*'), include=('*',)),
    # 需要安装的依赖
    install_requires=[
        'web3>=4.8.3',
        # 'ethereum==2.3.2',
        'eth-account',
        'eth-utils',
        'logbook'
    ],
    py_modules=['pycontractsdk'],
    python_requires='>=3.6',
    setup_requires=['setuptools-markdown'],
    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
    ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Topic :: Utilities",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=False
)