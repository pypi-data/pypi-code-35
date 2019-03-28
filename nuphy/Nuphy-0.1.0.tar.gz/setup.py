#!/usr/bin/env python
import os
from setuptools import setup, find_packages
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Nuphy",
    version='0.1.0',
    packages=find_packages(),
    package_data={'nuphy': ['data/*']},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/nuphy'],
    install_requires=['numpy==1.16.2','xvfbwrapper==0.2.9','matplotlib==3.0.3','scipy==1.2.1','pandas==0.24.2'],
)
 
