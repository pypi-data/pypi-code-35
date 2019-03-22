"""
Smoke Test the check_build module
"""

# Author: G Varoquaux
# License: BSD 3 clause

from h2o4gpu.__check_build import raise_build_error

from h2o4gpu.utils.testing import assert_raises


def test_raise_build_error():
    assert_raises(ImportError, raise_build_error, ImportError())
