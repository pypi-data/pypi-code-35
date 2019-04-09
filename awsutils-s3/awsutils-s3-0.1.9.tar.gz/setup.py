import os
from setuptools import setup, find_packages


name = 'awsutils-s3'


def get_version(version_file='_version.py'):
    """Retrieve the package version from a version file in the package root."""
    filename = os.path.join(os.path.dirname(__file__), 'awsutils', 's3', version_file)
    with open(filename, 'rb') as fp:
        return fp.read().decode('utf8').split('=')[1].strip(" \n'")


setup(
    name=name,
    version=get_version(),
    packages=find_packages(),
    namespace_packages=['awsutils'],
    install_requires=[
        'awscli',
        'tldextract',
        'validators'
    ],
    url='https://github.com/mrstephenneal/awsutils-s3',
    license='MIT',
    author='Stephen Neal',
    author_email='stephen@stephenneal.net',
    description='AWS Command Line Interface wrapper for S3 services.'
)
