"""
Setup script for ymldoc
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='dac',
    version='0.1.2',
    description="Atlantean's internal tool for Documentation (as Code)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/atlantean-code/dac',
    author='Dan Sikes',
    author_email='dsikes@atlantean.io',
    keywords='documentation as code',
    packages=find_packages(),
    install_requires=['docopt', 'jinja2', 'tabulate'],

    entry_points={
        'console_scripts': [
            'dac=cli.__main__:main',
        ],
    },

    project_urls={
        'Source': 'https://bitbucket.org/atlantean-code/dac',
    },
)