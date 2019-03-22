# -*- coding: utf-8 -*-

import sys
import re
import pathlib
import subprocess
from shutil import rmtree

from setuptools import find_packages, setup
from setuptools.command.upload import upload

base_dir = pathlib.Path(__file__).parent


def parse_file(file_path):
    with open(base_dir / file_path, encoding='utf-8') as f:
        return f.read().strip()


def find_version(path):
    contents = parse_file(path)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", contents, re.M)
    if version_match:
        return version_match.group(1)

    raise RuntimeError('Unable to find version string.')


readme = parse_file('README.md')
version = find_version('facture/__version__.py')


class UploadCommand(upload):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(f'{base_dir}/dist')
        except FileNotFoundError:
            pass

        self.status('Building Source distribution...')
        subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
        self.status('Uploading the package to PyPI via Twine...')
        subprocess.check_call(['twine', 'upload', 'dist/*'])
        self.status('Pushing git tags...')
        subprocess.check_call(['git', 'tag', f'v{version}'])
        subprocess.check_call(['git', 'push', '--tags'])


required = [
    "sanic>=18.12.0",
    "aiohttp>=4.0.0a0",
    "aiopg>=0.16.0",
    "psycopg2-binary>=2.7.7",
    "marshmallow>=3.0.0rc4",
    "peewee-async>=0.6.0a0",
    "peewee>=3.9.2",
    "apispec>=1.0.0",
    "ujson>=1.35",
    "uvloop>=0.12.1"
]

setup(
    name='facture',
    version=version,
    description='Framework for building Web APIs using asyncio',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Robert Wikman',
    author_email='rbw@vault13.org',
    url='https://github.com/rbw/facture',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': [
        ]
    },
    package_data={
        '': ['LICENSE'],
    },
    python_requires='>=3.6',
    setup_requires=['pipenv'],
    install_requires=required,
    include_package_data=True,
    license='BSD-2',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
