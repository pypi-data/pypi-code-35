import os
import shutil
import sys

from oly.docker import Docker
from oly.utils import Utils

py_version = sys.version_info[:2]

if py_version < (2, 7):
    raise RuntimeError('On Python 2, Supervisor requires Python 2.7 or later')
elif (3, 0) < py_version < (3, 4):
    raise RuntimeError('On Python 3, Supervisor requires Python 3.4 or later')

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


if not os.path.isdir(Utils.OLY_HOME):
    os.mkdir(Utils.OLY_HOME)

if not os.path.isdir(Utils.TOOLS_DIR):
    shutil.copytree(os.path.join('oly', 'tools'), Utils.TOOLS_DIR)


if not os.path.isdir(Utils.PROJECTS_DIR):
    os.mkdir(Utils.PROJECTS_DIR)

Docker.create_network()

version_txt = os.path.join(here, 'oly', 'version.txt')
oly_version = open(version_txt).read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="oly",
    version=oly_version,
    author="Genci Likaj",
    author_email="genci.likaj@gmail.com",
    license='MIT',
    packages=[
        'oly',
        'oly.tools',
        'oly.tools.mysql',
        'oly.tools.postgres',
        'oly.tools.mongo',
        'oly.tools.rabbitmq',
        'oly.tools.redis',
        'oly.tools.swagger',
    ],
    package_dir={'oly': 'oly'},
    package_data={
        'oly': ['*.txt'],
        'oly.tools.mysql': ['*'],
        'oly.tools.postgres': ['*'],
        'oly.tools.mongo': ['*'],
        'oly.tools.rabbitmq': ['*'],
        'oly.tools.redis': ['*'],
        'oly.tools.swagger': ['*'],
    },
    install_requires=['click', 'requests', 'tabulate'],
    entry_points={
        'console_scripts': ['oly = oly.cli:start']
    },
    description = "Oly Cli",
    long_description = long_description,
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
)