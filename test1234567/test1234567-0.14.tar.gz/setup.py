# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname

PACKAGE = "test1234567"
NAME = "test1234567"
DESCRIPTION = "test1234567 description"
AUTHOR = "vitaliyrakitin"
AUTHOR_EMAIL = "vitaliyrakitin@ya.ru"
URL = ""
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author=AUTHOR,
    packages=find_packages(),
    author_email=AUTHOR_EMAIL,
    url=URL,
    zip_safe=True
)
