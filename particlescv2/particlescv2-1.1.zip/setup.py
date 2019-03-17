#!/usr/bin/env python
from distutils.core import setup

setup(
    name='particlescv2',
    version='1.1',
    author='Andreas Bunkahle',
    author_email='abunkahle@t-online.de',
    description='Port of the Pygame PyIgnition 1.0 Particles Engine library to OpenCV2',
    license='MIT',
    py_modules=['particlescv2'],
    python_requires='>=2.7',
    url='https://github.com/bunkahle/particlescv2',
    long_description=open('README.txt').read(),
    platforms = ['any'],
    install_requires=['blist', 'numpy', 'opencv-python']
)
