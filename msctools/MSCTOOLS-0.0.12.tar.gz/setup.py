#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='MSCTOOLS',
      version='0.0.12',
      description='moyan private tools',
      author='moyan',
      author_email='ice.moyan@gmail.com',
      packages=find_packages(),
      include_package_data=True,
)

''''
name/version: 是整个项目的名字，打包后会使用此名字和版本号。
description: 是一个简短的对项目的描述，一般一句话就好，会显示在pypi上名字下端。
long_description: 是一个长的描述，相当于对项目的一个简洁，如果此字符串是rst格式的，PyPI会自动渲染成HTML显示。这里可以直接读取README.rst中的内容。
url: 包的连接，通常为GitHub上的链接或者readthedocs的链接。
packages: 需要包含的子包列表，setuptools提供了find_packages()帮助我们在根路径下寻找包，这个函数distutil是没有的。
          需要处理的包目录（包含__init__.py的文件夹） 
install_requires: 申明依赖包，安装包时pip会自动安装：格式如下（我上面的setup.py没有这个参数，因为我不依赖第三方包
      install_requires=[
        'Twisted>=13.1.0',
        'w3lib>=1.17.0',
        'queuelib',
        'lxml',
        'pyOpenSSL',
        'cssselect>=0.9',
        'six>=1.5.2',
        'parsel>=1.1',
        'PyDispatcher>=2.0.5',
        'service_identity',
    ]
py_modules 需要打包的python文件列表
'''


''''
#!/usr/bin/env python
# coding=utf-8
from setuptools import setup
# 把redis服务打包成C:\Python27\Scripts下的exe文件
setup(
    name="RedisRun",  #pypi中的名称，pip或者easy_install安装时使用的名称
    version="1.0",
    author="Andreas Schroeder",
    author_email="andreas@drqueue.org",
    description=("This is a service of redis subscripe"),
    license="GPLv3",
    keywords="redis subscripe",
    url="https://ssl.xxx.org/redmine/projects/RedisRun",
    packages=['DrQueue'],  # 需要打包的目录列表

    # 需要安装的依赖
    install_requires=[
        'redis>=2.10.5',
    ],

    # 添加这个选项，在windows下Python目录的scripts下生成exe文件
    # 注意：模块与函数之间是冒号:
    entry_points={'console_scripts': [
        'redis_run = DrQueue.RedisRun.redis_run:main',
    ]},

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
'''

