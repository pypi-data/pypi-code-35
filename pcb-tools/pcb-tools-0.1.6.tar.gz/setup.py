#!/usr/bin/env python

from setuptools import setup


def long_description():
    with open('README.rst') as fd:
        return fd.read()

    
setup(
    # TODO: rename to actual module name or rename module
    name='pcb-tools',
    version='0.1.6',
    author='Paulo Henrique Silva, Hamilton Kibbe',
    author_email='ph.silva@gmail.com, ham@hamiltonkib.be',
    description='Utilities to handle Gerber (RS-274X) files.',
    license='Apache',
    keywords='pcb gerber tools',
    url='http://github.com/curtacircuitos/pcb-tools',
    packages=['gerber', 'gerber.render'],
    long_description=long_description(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apple Public Source License',
    ],
    install_requires=['cairocffi~=0.6'],
)
