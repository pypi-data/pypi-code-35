from os import path
from setuptools import setup

# This call to setup() does all the work
setup(
    name='sfmc-to-json',
    version="0.2.5",
    description="Used to format FuelSDK reponses into JSON",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emailrhoads/sfmc_response_to_json",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=["salesforce_to_json"],
    include_package_data=True,
    install_requires=["suds"]
)