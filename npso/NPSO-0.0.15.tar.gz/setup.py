import os
os.environ["MLPCONFIGDIR"] = "."

from NPSO import config

from setuptools import setup, find_packages

LICENSE = 'MIT'

setup(
    name = config.__name__,
    version = config.__version__,
    LICENSE = LICENSE,
    author = config.__author__,
    author_email = 'zsexton@stanford.edu',
    url = 'https://github.com/zasexton/PyPso',
    download_url = 'https://github.com/zasexton/PyPso',
    packages = find_packages(exclude=['Doc']),
    install_requires = [
    'numpy>=1.14.2',
    'sympy>=1.1.1',
    'matplotlib>=2.2.2',
    ],
    classifiers = [
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.6',
    'Topic :: Scientific/Engineering',
    'Operating System :: MacOS',
    ]
)
