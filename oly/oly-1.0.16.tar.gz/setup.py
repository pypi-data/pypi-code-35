import os
import sys

py_version = sys.version_info[:2]

if py_version < (2, 7):
    raise RuntimeError('On Python 2, Supervisor requires Python 2.7 or later')
elif (3, 0) < py_version < (3, 4):
    raise RuntimeError('On Python 3, Supervisor requires Python 3.4 or later')

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

version_txt = os.path.join(here, 'oly', 'version.txt')
oly_version = open(version_txt).read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oly",
    version=oly_version,
    author="Genci Likaj",
    author_email="genci.likaj@gmail.com",
    description="Oly Cli",
    long_description=long_description,
    license='MIT',
    packages=find_packages(),
    package_dir={'oly': 'oly'},
    install_requires=['click', 'requests', 'tabulate'],
    include_package_data=True,
    zip_safe=False,
    long_description_content_type = "text/markdown",
    url = "https://github.com/glikaj/oly",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://github.com/glikaj/oly/',
        'Tracker': 'https://github.com/glikaj/oly/issues',
    },
    keywords='cli development console docker',
    entry_points={
        'console_scripts': ['oly = oly.cli:start']
    },
)