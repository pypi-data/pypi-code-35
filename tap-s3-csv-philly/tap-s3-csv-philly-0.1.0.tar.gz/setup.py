#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-s3-csv-philly",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Stitch",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_s3_csv_philly"],
    install_requires=[
        "singer-python>=5.0.12",
        "requests==2.20.0",
        "boto3",
        "botocore",
    ],
    entry_points="""
    [console_scripts]
    tap-s3-csv-philly=tap_s3_csv_philly:main
    """,
    packages=["tap_s3_csv_philly"],
    package_data = {
        "schemas": ["tap_s3_csv_philly/schemas/*.json"]
    },
    include_package_data=True,
)
