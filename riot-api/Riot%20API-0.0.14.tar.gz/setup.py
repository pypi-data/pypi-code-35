from setuptools import setup, find_packages

name = "Riot API"
version = "0.0.14"
author = "Kristian Alexander Weatherhead"
url = "https://github.com/Alex-Weatherhead/riot_api"
packages = find_packages()
description = "A thin wrapper around the Riot Games API for League of Legends."
with open("README.rst", "r") as f:
    long_description = f.read()
long_description_content_type="text/x-rst"
license="LICENSE"
install_requires = [
    "requests >= 2.20.1"
]
test_suite = "tests"

setup(
    name=name,
    version=version,
    author=author,
    url=url,
    packages=packages,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    license=license,
    install_requires=install_requires,
    test_suite=test_suite
)