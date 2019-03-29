"""Application setup."""

import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='brighthive-authlib',
    version='1.0.1',
    author='Gregory Mundy',
    author_email='greg@brighthive.io',
    description='BrightHive API Authorization and Authentication Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brighthive/authlib',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',
        'python-jose-cryptodome',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
