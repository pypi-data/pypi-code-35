# Reference: https://github.com/pypa/sampleproject/blob/master/setup.py
# this meant to be used with create-pip-package.sh gist and gex.

from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

def requirements():
    """Returns packages required by current project."""
    reqs = []
    if os.path.exists('requirements.txt') and os.path.isfile('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            for line in f:
                if line.startswith('git+https'):
                    continue
                reqs.append(line.strip())
    return reqs


def packages():
    """Returns list of packages inside current project."""
    return find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])


setup(
    name='ingi-cli',
    version='0.1.1',
    description='A CLI tool for gists like no other. Run, download and help build a searchable gist API',
    author='Ian Loubser',
    author_email='loubser.ian@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages(),
    install_requires=requirements(),
    entry_points={
        'console_scripts': [
            'ingi=ingi.run:main'
        ]
    }
)
