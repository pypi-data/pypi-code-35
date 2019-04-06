"""
Provide implementation of the PyPi version checking configurations manipulating.
"""
import os

import yaml
from accessify import private

from pypi_version.constants import PYPI_VERSION_CONFIG_FILE_NAME


class ConfigParameters:
    """
    Configuration parameters data transfer object.
    """

    def __init__(self, package_name, ci_name, development_branch, release_branch):
        self._package_name = package_name
        self._ci_name = ci_name
        self._development_branch = development_branch
        self._release_branch = release_branch

    @property
    def package_name(self):
        """
        Get configuration file's package name.
        """
        return self._package_name

    @property
    def ci_name(self):
        """
        Get configuration file's continuous integration name.
        """
        return self._ci_name

    @property
    def development_branch(self):
        """
        Get configuration file's package development branch.
        """
        return self._development_branch

    @property
    def release_branch(self):
        """
        Get configuration file's package release branch.
        """
        return self._release_branch


class ConfigFile:
    """
    Implementation of PyPi version configuration file.
    """

    @property
    def path(self):
        """
        Get the system path where parsing configuration file was called.
        """
        return os.getcwd()

    @private
    def read(self, name=PYPI_VERSION_CONFIG_FILE_NAME):
        """
        Read configuration file.

        Return dictionary.
        """
        with open(self.path + '/.' + name + '.yml') as f:
            return yaml.safe_load(f)

    def parse(self):
        """
        Parse configuration file.
        """
        config_as_dict = self.read()

        return ConfigParameters(
            package_name=config_as_dict.get('package').get('name'),
            ci_name=config_as_dict.get('ci').get('name'),
            development_branch=config_as_dict.get('branches').get('development'),
            release_branch=config_as_dict.get('branches').get('release'),
        )
