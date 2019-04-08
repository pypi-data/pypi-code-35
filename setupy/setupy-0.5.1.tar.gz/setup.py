import os
import sys
from os import path
from shutil import rmtree

from setuptools import Command, find_packages, setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')
        
        sys.exit()


VERSION = open("VERSION.txt").read()


def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r


base = {
    "name": "mypackage",
    "version": "0.1.0",
    "packages": find_packages(exclude=['contrib', 'docs', 'test'])
}

add_upload_command = {
    "cmdclass": {
        "upload": UploadCommand
    }
}

add_long_description = {
    "long_description": long_description,
    "long_description_content_type": "text/markdown"
}

setupy = {
    "name": "setupy",
    "version": VERSION,
    "install_requires": ["isort>=4.3", "pyyaml>=3.13", "flask>=1.0.2"],
    "extras_require": {
        "dev": ["pytest", "pytest-cov"],
        "neovim": ["neovim"]
    }
}



setup(**merge(base, add_upload_command, add_long_description, setupy))
