#!/usr/bin/env python3
from setuptools import setup

def get_readme():
    with open('README.md', 'r') as readme:
        return readme.read()

setup(
    name='bonnibel',
    version='0.1',
    description='Build script generator for the Popcorn kernel',
    long_description=get_readme(),
    keywords=['build', 'ninja', 'generator'],
    url='https://github.com/justinian/bonnibel',
    author='Justin C. Miller',
    author_email='justin@devjustinian.com',
    license='MIT',
    packages=['bonnibel'],
    scripts=['bin/pb'],
    install_requires=['jinja2', 'PyYAML'],
    include_package_data=True,
    zip_safe=False
    )
