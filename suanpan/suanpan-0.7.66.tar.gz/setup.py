#!/usr/bin/env python

"""
suanpan
"""

import itertools
import os
import re

from setuptools import find_packages, setup

VERSION_PARRTERN = r"__version__ = \"([\d\w\.]*)\""
VERSION_FILE = os.path.join("suanpan", "__init__.py")
VERSION = re.findall(VERSION_PARRTERN, open(VERSION_FILE, "r").read())[0]

BASE_REQUIRES = [
    "imageio==2.4.1",
    "numpy==1.15.2",
    "opencv-python==3.4.3.18",
    "pandas==0.23.4",
    "tqdm==4.28.1",
    "retrying==1.3.3",
    "pyodps==0.8.0",
    "tabulate==0.8.3",
    "colorama==0.4.1",
    "lostc==0.1.0",
    "addict==2.2.0",
]
SKLEARN_REQUIRES = [
    "scikit-learn==0.20.2",
    "matplotlib==3.0.2",
    "sklearn2pmml==0.42.0",
    "sklearn_pandas==1.8.0",
    "xgboost==0.81",
]
HIVE_REQUIRES = [
    "sasl==0.2.1",
    "thrift-sasl==0.3.0",
    "thrift==0.11.0",
    "pyhive[hive]==0.6.1",
]
GRPC_REQUIRES = ["googleapis-common-protos==1.6.0b9", "grpcio-tools==1.19.0"]
OSS2_REQUIRES = ["oss2==2.6.1"]
MINIO_REQUIRES = ["minio==4.0.11"]
REDIS_REQUIRES = ["redis==3.2.0"]
INSTALL_REQUIRES = BASE_REQUIRES
EXTRAS_REQUIRES = {
    "service": list(
        itertools.chain(OSS2_REQUIRES, MINIO_REQUIRES, HIVE_REQUIRES, GRPC_REQUIRES)
    ),
    "docker": list(
        itertools.chain(
            OSS2_REQUIRES,
            MINIO_REQUIRES,
            HIVE_REQUIRES,
            REDIS_REQUIRES,
            SKLEARN_REQUIRES,
        )
    ),
    "stream": list(
        itertools.chain(OSS2_REQUIRES, MINIO_REQUIRES, HIVE_REQUIRES, REDIS_REQUIRES)
    ),
}
README = "README.md"


def read_file(path):
    with open(path, "r") as f:
        return f.read()


fix_packages = ["__suanpan__"]
packages = find_packages()
packages.extend(fix_packages)

setup(
    name="suanpan",
    version=VERSION,
    packages=packages,
    license="See License",
    author="majik",
    author_email="me@yamajik.com",
    description=read_file(README),
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRES,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
