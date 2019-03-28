from setuptools import setup, find_packages
import io
import re

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

with io.open("surfing_libs/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

setup(
    name="surfing_lib",
    version=version,
    author="surfing",
    author_email="surfing@surfingtech.cn",
    description="公司公用库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
