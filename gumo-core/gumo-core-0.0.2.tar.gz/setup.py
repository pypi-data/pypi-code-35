import os
import setuptools


name = 'gumo-core'
with open(os.path.join('..', 'gumo_version.txt'), 'r') as fh:
    version = fh.read().strip()

description = 'Gumo Core Library'
dependencies = [
    'pyyaml >= 5.1',
    'injector >= 0.13.1',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = [
    package for package in setuptools.find_packages()
    if package.startswith('gumo')
]

namespaces = ['gumo', 'gumo.core']

setuptools.setup(
    name=name,
    version=version,
    author="Gumo Project Team",
    author_email="gumo-organizer@levii.co.jp",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gumo-py/gumo",
    packages=packages,
    namespaces=namespaces,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
)
