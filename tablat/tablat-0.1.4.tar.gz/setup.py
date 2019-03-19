# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path
import re


# Get current version
version = '0.1.4'
version_input_path = Path('./setup/version.txt')
if version_input_path.exists():
    with open(version_input_path, 'r') as f:
        version_input = f.readline().rstrip()

    if re.match('\\d+\\.\\d+\\.\\d+', version_input):
        version = version_input

# Load doc
with open('README.md') as f:
    readme = f.read()

setup(
    name='tablat',
    version=version,
    description='Print basic tables in python',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='salpreh',
    author_email='salva.perez46@gmail.com',
    url='https://github.com/salpreh/tablat',
    license='MIT License',
    packages=find_packages(exclude=('test', 'assets', 'venv', 'doc'))
)
