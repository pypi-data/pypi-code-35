# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="SimTtrading",
    version="1.0.2",
    description='实现撮合交易并模拟下单',
    author='miao',
    author_email='miaochong1521@163.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        ],
)
