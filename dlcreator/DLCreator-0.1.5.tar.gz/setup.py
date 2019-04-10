#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup, find_packages

setup(
    name="DLCreator",
    version="0.1.5",
    keywords=("deep learning", "tool"),
    description="One-line command to generate a deep learning folder structure and code template!",
    long_description=open('README.md').read(),
    license="MIT Licence",
    url="https://github.com/nghuyong/DLCreator",
    author="nghuyong",
    author_email="nghuyong@163.com",
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    platforms="any",
    install_requires=[
        'pyfiglet',
        'termcolor'
    ],
    scripts=[],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    entry_points={
        'console_scripts': [
            'DLCreator = DLCreator.command:run',
        ]
    }
)
