#! /usr/bin/env python3

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="crossclip",
    version="0.2.1",
    author="Charlie Sale",
    author_email="softwaresale01@gmail.com",
    description="A Cross Platform clipboard manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/softwaresale/crossclip",
    packages=setuptools.find_packages(),
    install_requires=[
        'Pillow',
    ],
    extras_require={
        'GTK': ['pygobject'],
        'Qt': ['PyQt5'],
    },
    test_suite='nose.collector',
    tests_require=['nose', 'numpy'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
)
