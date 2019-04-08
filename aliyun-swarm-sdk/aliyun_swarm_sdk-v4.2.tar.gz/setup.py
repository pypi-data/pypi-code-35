#coding: utf8
from distutils.core import setup
import os
import sys

REQUIRED_PYTHON = (3, 6)

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='aliyun_swarm_sdk',                #需要打包的名字
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    version='v4.2',                         #版本
    packages=['aliyun_swarm_sdk', 'aliyun_swarm_sdk'], #需要打包的模块
    author="eagle",                         #作者
    author_email="1032231418@qq.com",        #邮箱
    license="Apache License Version 2.0",
    description="阿里云 swarm SDK",
    classifiers=[
                      "Programming Language :: Python :: 3",
                      "License :: OSI Approved :: MIT License",
                      "Operating System :: OS Independent",
                  ],
    long_description=read('README.rst'),
    project_urls={
        'Source': 'https://github.com/1032231418/aliyun_swarm_sdk',
    },
)