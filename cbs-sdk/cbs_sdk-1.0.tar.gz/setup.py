# -*- coding: utf-8 -*-
# IDE PyCharm
# FileName setup.py
# Created by wudonghai on 13:48
from setuptools import setup

'''
把redis服务打包成C:\Python27\Scripts下的exe文件
'''
files = ["Application/*"]
setup(
    name="cbs_sdk",  #pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    version="1.0",
    author="chinabanksoft",
    author_email="andreas@drqueue.org",
    description=("This is a service of cbs sdk"),
    license="chinabanksoft",
    keywords="cbs sdk",
    # url="https://",
    packages=["Application", "Application/src", "Application/static"], # 需要打包的目录列表
    include_package_data=True,
    package_data={"Application": ["Application/**"]},
    # 需要安装的依赖
    install_requires=[
        'redis>=3.2.1',
        'pymongo>=3.7.2',
        'tornado>=6.0.2',
        'motor>=2.0.0',
        'setuptools>=39.1.0',
    ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    # entry_points={'console_scripts': [
    #     'redis_run = RedisRun.redis_run:main',
    # ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)