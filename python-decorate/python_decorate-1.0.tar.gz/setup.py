# coding=utf-8

__author__ = 'songmengyun'

from setuptools import setup

setup(
    name = "python_decorate",          # 包名
    version = "1.0",              # 版本信息
    packages = ['python_decorate'],  # 要打包的项目文件夹
    include_package_data=True,    # 自动打包文件夹内所有数据
    zip_safe=True,                # 设定项目包为安全，不用每次都检测其安全性
    url='http://www.hujiang.com',

    install_requires = [          # 安装依赖的其他包
    # 'Flask>=0.10',
    'requests',
    ],

    # 应用依赖的包无法从PyPI中获取怎么办，我们需要指定其下载路径：
    # dependency_links=[    # 依赖包下载路径
    #     'http://example.com/dependency.tar.gz'
    # ]

    # 设置程序的入口为hello
    # 安装后，命令行执行hello相当于调用hello.py中的main方法
    # entry_points={
    #     'console_scripts':[
    #         'hello = myapp.hello:main'
    #     ]
    #  },

    # 如果要上传到PyPI，则添加以下信息
    author = "songmengyun",
    author_email = "526955572@qq.com",
    # description = "This is an Example Package",
    # license = "MIT",
    # keywords = "hello world example examples",
    # url = "http://example.com/HelloWorld/",
 )