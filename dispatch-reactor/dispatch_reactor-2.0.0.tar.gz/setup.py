from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'dispatch_reactor',
    scripts=['bin/dispatcher'],
    packages=['dispatch'],
    version = '2.0.0',
    description = 'Module for dispatching jobs and timed operations',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'KJ',
    author_email = 'jdotpy@users.noreply.github.com',
    url = 'https://github.com/jdotpy/dispatch',
    download_url = 'https://github.com/jdotpy/dispatch/tarball/master',
    keywords = ['tools'],
    classifiers = [
        "Programming Language :: Python :: 3",
    ],
)
