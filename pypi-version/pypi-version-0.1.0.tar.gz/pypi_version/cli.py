"""
Provide implementation of the command line interface.
"""
import sys

import click

from pypi_version.config import ConfigFile
from pypi_version.constants import (
    PYPI_VERSION_CHECKING_FAILED_SYS_CODE,
    PYPI_VERSION_CHECKING_PASSED_SYS_CODE,
)
from pypi_version.main import (
    PullRequest,
    PypiPackageVersion,
)
from pypi_version.utils import (
    get_package_to_check_version,
    install_package_to_check,
)


@click.group()
@click.version_option(version='0.1.0')
@click.help_option()
def cli():
    """
    Command line interface for PyPi version checking.
    """
    pass


@cli.command()
def check():
    """
    Check if you haven't forgotten to bump the PyPi package version.
    """
    install_package_to_check()

    config = ConfigFile().parse()
    parsed_package_version = get_package_to_check_version(name=config.package_name)

    if not PullRequest().is_for_check(
            ci_name=config.ci_name,
            develop_branch=config.development_branch,
            release_branch=config.release_branch,
    ):
        sys.exit(PYPI_VERSION_CHECKING_PASSED_SYS_CODE)

    if PypiPackageVersion.does_exist(name=config.package_name, version=parsed_package_version):
        sys.exit(PYPI_VERSION_CHECKING_FAILED_SYS_CODE)

    sys.exit(PYPI_VERSION_CHECKING_PASSED_SYS_CODE)
