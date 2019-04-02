import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Jin-Py",
    version = "1.0.0",
    author = "Judah Caruso Rodriguez",
    author_email = "judah@tuta.io",
    description = ("A git/mercurial-flavored wrapper for rsync."),
    license = "MIT",
    keywords = "jin git mercurial rsync wrapper",
    url = "",
    long_description=read("readme.md"),
    packages = ["jin"],
    install_requires = [
        "watchdog>=0.9.0",
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Version Control :: Mercurial",
    ],
)
