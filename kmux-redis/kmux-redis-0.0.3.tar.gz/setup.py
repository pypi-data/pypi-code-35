# -*- coding:utf-8 -*-

import setuptools

setuptools.setup(
    name="kmux-redis",
    version="0.0.3",
    keywords=("redis",),
    author="Mu Xiaofei",
    author_email="me@muxiaofei.cn",
    description="redis client",
    long_description="",
    long_description_content_type="text/x-rst",
    url="https://gitee.com/muxiaofei/kmux-redis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["redis"],
)
