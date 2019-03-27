import os
import setuptools


name = 'gumo-task-emulator'
with open(os.path.join('..', 'gumo_version.txt'), 'r') as fh:
    version = fh.read().strip()

description = 'Gumo Task Emulator Library'
dependencies = [
    f'gumo-core >= {version}',
    f'gumo-datastore >= {version}',
    f'gumo-task >= {version}',
    'Flask >= 1.0.2',
    'flasgger >= 0.9.1',
]

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()

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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=dependencies,
)
