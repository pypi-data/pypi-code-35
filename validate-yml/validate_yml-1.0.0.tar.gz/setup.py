# -*- coding:utf-8 -*-
__author__ = 'jimmy'
__date__ = '2019/3/4'
from setuptools import setup, find_packages

setup(
    name="validate_yml",
    version="1.0.0",
    packages=find_packages(),

    description="validate yml syntax",
    long_description="validate yml syntax, return OK only if syntax correct",
    author="jimmy",
    author_email="zjm901026@163.com",

    license="GPL",
    keywords=("validate", "yml"),
    platforms="Independant",
    url="",
    install_requires=[
        "pyyaml",
    ],
    entry_points={
        'console_scripts': [
            'validate_yml = validate_yml.main:main',
        ]
    }
)
