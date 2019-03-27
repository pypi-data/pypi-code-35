# -*- coding: utf-8 -*-
# created by inhzus

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='juq',
    version='1.0',
    author='Zhi Sun',
    author_email='inhzus@gmail.com',
    description='Yuque SDK and command line tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/inhzus/juq',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    entry_points={
        'console_scripts': ['juq=juq.caller:run']
    }
)
