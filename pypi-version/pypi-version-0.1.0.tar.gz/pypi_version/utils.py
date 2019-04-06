"""
Provide implementation of the utils for PyPi version checking.
"""
import os

import pkg_resources


def install_package_to_check():
    """
    Build and install the package.

    Is used to fetch the package version provided to pull request.
    """
    os.system('python3 setup.py sdist > /dev/null')
    os.system('pip3 install dist/*.tar.gz > /dev/null')


def get_package_to_check_version(name):
    """
    Get package version.
    """
    return pkg_resources.require(name)[0].version
