import os
import dhttp

from setuptools import setup


version = dhttp.DHTTP_VERSION

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dhttp",
    version = "0.1.0",
    author = "Gustavo Rehermann",
    author_email = "rehermann6046@gmail.com",
    description = ("A simple, but dynamic, decorator-based HTTP server inspired by Node.js's Express."),
    license = "MIT",
    keywords = "http server httpd express decorator simple easy dynamic",
    packages=['dhttp'],
    long_description=read('README.md'),
    classifiers=[
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "License :: OSI Approved :: MIT License",
    ],
)