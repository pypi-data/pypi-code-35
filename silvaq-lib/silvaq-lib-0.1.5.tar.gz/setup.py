from setuptools import setup
import io
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

with io.open("silvaq_libs/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \'(.*?)\'", f.read()).group(1)

setup(
    name="silvaq-lib",
    version=version,
    author="silvaq",
    author_email="babbage@hotmail.com",
    description="个人常用功能封装",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SilvaQ/silvaq-pylib",
    packages=['silvaq_libs'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
