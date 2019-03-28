# -*- coding:utf-8 -*-

import setuptools

setuptools.setup(
    name="kmux-mongo",
    version="0.0.2",
    keywords=("mongo",),
    author="Mu Xiaofei",
    author_email="me@muxiaofei.cn",
    description="mongo client",
    long_description="",
    long_description_content_type="text/x-rst",
    url="https://gitee.com/muxiaofei/kmux-mongo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["bson", "pymongo"],
)
