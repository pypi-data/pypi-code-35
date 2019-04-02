#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import glob
import hashlib
import os

import six
import responses

from hatcher.errors import ChecksumMismatchError, InvalidRuntime
from hatcher.testing import (
    runtime_from_metadata,
    RUNTIME_CPYTHON_2_7_10_RH5_X86_64_METADATA)

from hatcher.core.url_templates import URLS_V1
from hatcher.core.tests.v0.base_test_repository import (
    BaseTestRepository as BaseTestRepositoryV0)


class BaseTestRepository(BaseTestRepositoryV0):

    api_version = 1
    urls = URLS_V1

    # replaced tests #################################################

    @responses.activate
    def test_list_runtimes(self):
        # Given
        expected = [(u'cpython', u'2.7.10+1',),
                    (u'cpython', u'3.4.3+2',)]
        platform_name = 'rh5-x86_64'
        platform = self.repository.platform(platform_name)
        self.brood_responses.test_list_runtimes()

        # When
        metadata = platform.list_runtimes()

        # Then
        six.assertCountEqual(self, metadata, expected)

    @responses.activate
    def test_runtime_index(self):
        # Given
        given_index = {
            "cpython": {
                "2.7.10+1": {
                    "abi": "gnu",
                    "filename": "cpython-2.7.10+1-rh5_x86_64-gnu.runtime",
                    "implementation": "cpython",
                    "language_version": "2.7.10",
                    "platform": "rh5-x86_64",
                    "sha256": "81ec4d15bd8b131c80eb72cb0f5222846e306bb3f1dd8ce572ffbe859ace1608",  # noqa
                    "version": "2.7.10+1",
                },
                "3.4.3+2": {
                    "abi": "gnu",
                    "filename": "cpython-3.4.3+2-rh5_x86_64-gnu.runtime",
                    "implementation": "cpython",
                    "language_version": "3.4.3",
                    "platform": "rh5-x86_64",
                    "sha256": "2846e306bb3f1dd8ce572ffbe859ace160881ec4d15bd8b131c80eb72cb0f522",  # noqa
                    "version": "3.4.3+2",
                },
            },
        }

        platform_name = 'rh5-x86_64'
        self.brood_responses.test_runtime_index(given_index, platform_name)

        platform = self.repository.platform(platform_name)

        # When
        obtained_index = platform.runtime_index()

        # Then
        self.assertEqual(obtained_index, given_index)

    @responses.activate
    def test_runtime_metadata(self):
        # Given
        implementation = 'cpython'
        version = '2.7.10+2'
        platform_name = 'rh5-x86_64'
        platform = self.repository.platform(platform_name)
        expected = {
            "abi": "gnu",
            "build_revision": "2e27fc462cb45fd6cbce0000b62e2d89923e2449",
            "filename": "cpython-2.7.10+2-rh5_x86_64-gnu.runtime",
            "implementation": implementation,
            "language_version": "2.7.10",
            "metadata_version": "1.0",
            "platform": platform_name,
            "sha256": "671cea9617ac71a577b8d76b17a29a96cd9f366b74d09e8474393d465a0c4489",  # noqa
            "version": version}
        self.brood_responses.test_runtime_metadata(expected)

        # When
        metadata = platform.runtime_metadata(implementation, version)

        # Then
        self.assertEqual(metadata, expected)

    @responses.activate
    def test_upload_runtime(self):
        # Given
        filepath = runtime_from_metadata(
            self.temp_dir, RUNTIME_CPYTHON_2_7_10_RH5_X86_64_METADATA)
        self.brood_responses.test_upload_runtime('rh5_x86_64')

        # When
        self.repository.upload_runtime(filepath)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_runtime_v1.json')
        self.assertRegexpMatches(request.url, r'^.*?\?overwrite=False$')

    @responses.activate
    def test_upload_runtime_force(self):
        # Given
        filepath = runtime_from_metadata(
            self.temp_dir, RUNTIME_CPYTHON_2_7_10_RH5_X86_64_METADATA)
        self.brood_responses.test_upload_runtime_force('rh5_x86_64')

        # When
        self.repository.upload_runtime(filepath, overwrite=True)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_runtime_v1.json')
        self.assertRegexpMatches(request.url, r'^.*?\?overwrite=True$')

    # new tests ######################################################

    @responses.activate
    def test_upload_runtime_not_zipfile(self):
        # Given
        filename = 'runtime'
        data = 'python'
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as fh:
            fh.write(data)

        # When/Then
        with self.assertRaises(InvalidRuntime):
            self.repository.upload_runtime(filepath)
