"""
Setup the package.
"""
from setuptools import find_packages, setup

DESCRIPTION = \
    'Check if you haven\'t forgotten to bump the PyPi package version number before you merge a release pull request.'

with open('README.md', 'r') as read_me:
    long_description = read_me.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    version='0.1.0',
    name='pypi-version',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dmytrostriletskyi/pypi-version',
    license='MIT',
    author='Dmytro Striletskyi',
    author_email='dmytro.striletskyi@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pypi-version = pypi_version.cli:cli',
        ]
    },
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
