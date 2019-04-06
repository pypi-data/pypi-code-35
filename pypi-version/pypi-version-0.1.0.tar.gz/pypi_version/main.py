"""
Provide implementation of the PyPi version checking.
"""
import os

import requests
from accessify import private

from pypi_version.constants import (
    FETCH_PYPI_PACKAGE_URL,
    HTTP_STATUS_OK,
    TravisCi,
)
from pypi_version.errors import (
    NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE,
    NotSupportedContinuousIntegrationError,
)


class PypiPackageVersion:
    """
    Implementation of PyPi package version.
    """

    @staticmethod
    def does_exist(name, version):
        """
        Check if package with specified name and version already uploaded to the PyPi.

        Send request to the PyPi. If page is presented — package exist, else — does not exist.
        """
        response = requests.get(
            FETCH_PYPI_PACKAGE_URL.format(package_name=name, package_version=version),
        )

        if response.status_code == HTTP_STATUS_OK:
            return True

        return False


class PullRequest:
    """
    Implementation of pull request.
    """

    @private
    @staticmethod
    def get_ci(name):
        """
        Get continuous integration class with related data.
        """
        if name == TravisCi.NAME:
            return TravisCi

        raise NotSupportedContinuousIntegrationError(
            NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE.format(ci_name=name),
        )

    def is_for_check(self, ci_name, develop_branch, release_branch):
        """
        Check if current pull request match pull request data in the configuration file.

        If environment variable of pull request branch you want merge to is empty, it means
        continuous integration run the job for the just branch, not pull request.

        If current pull request branches matches pull request branches in the configuration file — return true,
        else — return false.
        """
        ci = self.get_ci(name=ci_name)

        if not os.environ.get(ci.ENV_VARIABLE_PR_BRANCH_TO_NAME):
            return False

        if release_branch != os.environ.get(ci.ENV_VARIABLE_PR_BRANCH_TO_NAME):
            return False

        if develop_branch != os.environ.get(ci.ENV_VARIABLE_PR_BRANCH_FROM_NAME):
            return False

        return True
