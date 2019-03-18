import pathlib
import re
from setuptools import setup
import sys

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
PACKAGE_NAME = "steffentools"

CONST_TEXT = (HERE / f"{PACKAGE_NAME}/const.py").read_text()
VERSION = re.search("__version__ = \"([^']+)\"", CONST_TEXT).group(1)

setup(
    name="steffentools",
    version=VERSION,
    description="A collection of tools compiled for personal use.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="steffentools tools library",
    url="https://github.com/cmsteffen-code/steffentools",
    project_urls={
        "Source Code": "https://github.com/cmsteffen-code/steffentools",
        "Documentation": "https://steffentools.readthedocs.io/en/latest/",
    },
    author="CMSteffen",
    author_email="cmsteffen@protonmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[PACKAGE_NAME],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)
