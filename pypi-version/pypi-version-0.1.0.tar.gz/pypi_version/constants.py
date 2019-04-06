"""
Provide constants for PyPi version checking.
"""
PYPI_VERSION_CHECKING_PASSED_SYS_CODE = 0
PYPI_VERSION_CHECKING_FAILED_SYS_CODE = -1

PYPI_VERSION_CONFIG_FILE_NAME = 'pypi-version'
FETCH_PYPI_PACKAGE_URL = 'https://pypi.org/project/{package_name}/{package_version}/'

HTTP_STATUS_OK = 200


class TravisCi:
    """
    Travis continuous integration class with related data.
    """

    NAME = 'travis'
    ENV_VARIABLE_PR_BRANCH_FROM_NAME = 'TRAVIS_PULL_REQUEST_BRANCH'
    ENV_VARIABLE_PR_BRANCH_TO_NAME = 'TRAVIS_BRANCH'
