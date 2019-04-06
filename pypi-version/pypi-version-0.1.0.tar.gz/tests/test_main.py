"""
Provide tests for implementation of the PyPi version checking.
"""
import os

import pytest

from pypi_version.constants import (
    HTTP_STATUS_OK,
    TravisCi,
)
from pypi_version.errors import (
    NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE,
    NotSupportedContinuousIntegrationError,
)
from pypi_version.main import (
    PullRequest,
    PypiPackageVersion,
)


def test_pypi_package_version_exist(mocker, response):
    """
    Case: check if PyPi package version exists.
    Expect: true is returned.
    """
    response.status_code = HTTP_STATUS_OK

    mock_request_package = mocker.patch('requests.get')
    mock_request_package.return_value = response

    result = PypiPackageVersion.does_exist(name='Django', version='2.17.0')
    assert result is True


def test_pypi_package_version_does_not_exist(mocker, response):
    """
    Case: check if PyPi package version exists.
    Expect: false is returned.
    """
    response.status_code = None

    mock_request_package = mocker.patch('requests.get')
    mock_request_package.return_value = response

    result = PypiPackageVersion.does_exist(name='Django', version='14.1.5')
    assert result is False


def test_pull_request_is_for_check():
    """
    Case: check if pull request environment matches specified in the configuration file.
    Except: true is returned.
    """
    os.environ[TravisCi.ENV_VARIABLE_PR_BRANCH_FROM_NAME] = 'develop'
    os.environ[TravisCi.ENV_VARIABLE_PR_BRANCH_TO_NAME] = 'master'

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='develop', release_branch='master')
    assert result is True


def test_pull_request_is_for_check_not_supported_ci():
    """
    Case: check if pull request environment matches specified in the configuration file if CI isn't matched.
    Except: not supported continuous integration error.
    """
    expected_error_message = NOT_SUPPORTED_CONTINUOUS_INTEGRATION_ERROR_MESSAGE.format(ci_name='not-supported-ci')

    with pytest.raises(NotSupportedContinuousIntegrationError) as error:
        PullRequest().is_for_check(ci_name='not-supported-ci', develop_branch='develop', release_branch='master')

    assert expected_error_message == error.value.message


def test_pull_request_is_for_check_no_branch_to():
    """
    Case: check if pull request environment matches specified in the configuration file if is a branch job, not PR job.
    Except: false is returned.
    """
    os.environ[TravisCi.ENV_VARIABLE_PR_BRANCH_TO_NAME] = ''

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='develop', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_branch_from_unmatched():
    """
    Case: check if pull request environment matches specified in the configuration file if branch from isn't matched.
    Except: false is returned.
    """
    os.environ[TravisCi.ENV_VARIABLE_PR_BRANCH_FROM_NAME] = 'develop'

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='development', release_branch='master')
    assert result is False


def test_pull_request_is_for_check_branch_to_unmatched():
    """
    Case: check if pull request environment matches specified in the configuration file if branch to isn't matched.
    Except: false is returned.
    """
    os.environ[TravisCi.ENV_VARIABLE_PR_BRANCH_TO_NAME] = 'release'

    result = PullRequest().is_for_check(ci_name='travis', develop_branch='development', release_branch='master')
    assert result is False
