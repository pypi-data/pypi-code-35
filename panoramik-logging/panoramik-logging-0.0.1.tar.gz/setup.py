import os
import re

import setuptools

name = "panoramik-logging"
version_file = os.path.join(
    os.path.dirname(__file__),
    name.replace('-', '_'),
    '__init__.py'
)
with open(version_file) as vf:
    version = re.compile(
        r".*__version__ = '(.*?)'", re.S
    ).match(vf.read()).group(1)

setuptools.setup(
    name=name,
    version=version,
    description="Panoramik logging library",
    author="Khusain Orynbaev",
    author_email="suhain93@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
