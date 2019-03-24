# -*- coding:utf-8 -*-

import setuptools

with open("README.md", "r") as fo:
    long_description = fo.read()

with open("requirements.txt", 'r+') as fo:
    install_requires = fo.readlines()

setuptools.setup(
    name="kmux",
    version="0.0.1",
    keywords=("restful",),
    author="Mu Xiaofei",
    author_email="me@muxiaofei.cn",
    description="easy for restful development",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitee.com/muxiaofei/kmux",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
)
