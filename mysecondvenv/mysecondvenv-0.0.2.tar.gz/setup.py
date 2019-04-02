import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mysecondvenv",
    version = "0.0.2",
    author = "Antoine Marullaz",
    author_email = "antoine.marullaz@gmail.com",
    description = ("my second PypI package"),
    keywords = "example documentation tutorial",
    packages=['mysecondvenv'],
    url='',
    license="WTFPL",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
    ],
    long_description=read('README.md')
)