#!/usr/bin/env python3
"""
Setup script
"""

import os

from setuptools import find_packages, setup

def read(path):
    """
    Read a file
    """
    with open(path) as file_:
        return file_.read()

setup(
    name='cloudview',
    version='0.1.1',
    description="View instance information on all supported cloud providers",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author="Ricardo Branco",
    author_email='rbranco@suse.de',
    url='https://github.com/ricardobranco777',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=read('requirements.txt'),
    license='MIT License',
    zip_safe=False,
    keywords='cloudview',
    classifiers=[
        'Development Status :: 4 - Beta',  # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: '
        'MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
