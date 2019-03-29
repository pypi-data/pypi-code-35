import setuptools


name = 'gumo-task-emulator'
version = '0.0.9'
description = 'Gumo Task Emulator Library'
dependencies = [
    'gumo-core >= 0.0.13',
    'gumo-datastore >= 0.0.11',
    'gumo-task >= 0.0.8',
    'Flask >= 1.0.2',
    'flasgger >= 0.9.1',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = [
    package for package in setuptools.find_packages()
    if package.startswith('gumo')
]

namespaces = ['gumo']

setuptools.setup(
    name=name,
    version=version,
    author="Gumo Project Team",
    author_email="gumo-py@googlegroups.com",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gumo-py/gumo-task-emulator",
    packages=packages,
    namespaces=namespaces,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
    include_package_data=True,
    package_data={
        'gumo': ['*.yml', '*.html']
    },
)
