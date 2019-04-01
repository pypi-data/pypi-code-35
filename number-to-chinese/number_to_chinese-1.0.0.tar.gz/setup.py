import codecs
import os
import sys
 
try:
    from setuptools import setup
except:
    from distutils.core import setup
"""
打包的用的setup必须引入，
"""
 

with open("./README.md", "r") as fh:
    long_description = fh.read()

NAME = "number_to_chinese"
"""
名字，一般放你包的名字即可
"""
 
PACKAGES = ["number_to_chinese",]
"""
包含的包，可以多个，这是一个列表
"""
 
DESCRIPTION = "this is a Capital Chinese to Arabic numerals package."
"""
关于这个包的描述
"""

 
KEYWORDS = "chinese transform char number python package"
"""
关于当前包的一些关键字，方便PyPI进行分类。
"""
 
AUTHOR = "Wangyiyao"
"""
谁是这个包的作者，写谁的名字吧
我是MitchellChu，自然这里写的是MitchellChu
"""
 
AUTHOR_EMAIL = "1738698834@qq.com"
"""
作者的邮件地址
"""
 
URL = "http://blog.useasp.net/"
"""
你这个包的项目地址，如果有，给一个吧，没有你直接填写在PyPI你这个包的地址也是可以的
"""
 
VERSION = "1.0.0"
"""
当前包的版本，这个按你自己需要的版本控制方式来
"""
 
LICENSE = "MIT"
"""
授权方式，我喜欢的是MIT的方式，你可以换成其他方式
"""
 
setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    long_description=long_description,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
	"Operating System :: Microsoft :: Windows",
    	"Operating System :: MacOS",
    	"Operating System :: Unix",
	"Programming Language :: Python :: 2.7",
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
 
## 把上面的变量填入了一个setup()中即可。
