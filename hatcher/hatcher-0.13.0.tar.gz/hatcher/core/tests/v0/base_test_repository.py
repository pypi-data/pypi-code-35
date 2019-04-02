#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import glob
import hashlib
import json
import os
import re
import shutil
import tempfile

import responses
import six

from hatcher.errors import ChecksumMismatchError
from hatcher.testing import make_testing_egg, unittest
from hatcher.core.brood_url_handler import BroodURLHandler
from hatcher.core.model_registry import ModelRegistry
from hatcher.core.url_templates import URLS_V0
from hatcher.core.tests.common import JsonSchemaTestMixin


BODY_FILENAME_RE = re.compile(
    r'Content-Disposition: form-data; name="file"; filename="(.*?)"')


class BaseTestRepository(JsonSchemaTestMixin):

    api_version = 0
    urls = URLS_V0
    brood_responses = None
    repository = None

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix='hatcher-', suffix='-tmp')
        self.temp_dir2 = tempfile.mkdtemp(prefix='hatcher-', suffix='-tmp')
        self.url_handler = BroodURLHandler.from_auth('http://packages.enthought.com')
        self.model_registry = ModelRegistry(api_version=self.api_version)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.temp_dir2)

    @responses.activate
    def test_delete_repository(self):
        # Given
        self.brood_responses.test_delete_repository()

        # When
        self.repository.delete()

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        self.assertRegexpMatches(request.url, r'^.*?\?force=False$')

    @responses.activate
    def test_delete_repository_force(self):
        # Given
        self.brood_responses.test_delete_repository_force()

        # When
        self.repository.delete(force=True)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        self.assertRegexpMatches(request.url, r'^.*?\?force=True$')

    @unittest.expectedFailure
    @responses.activate
    def test_get_metadata(self):
        # Given
        expected = {}
        self.brood_responses.test_get_metadata(expected)

        # When
        metadata = self.repository.metadata()

        # Then
        self.assertEqual(metadata, expected)

    @unittest.expectedFailure
    @responses.activate
    def test_list_platforms(self):
        # Given
        expected = ['rh5-64', 'win-32', 'dos-16']
        self.brood_responses.test_list_platforms(expected)

        # When
        platform_names = self.repository.list_platforms()

        # Then
        self.assertEqual(platform_names, expected)

    @responses.activate
    def test_get_specific_platform(self):
        # Given
        platform_name = 'rh5-64'

        # When
        platform = self.repository.platform(platform_name)

        # Then
        self.assertEqual(platform.name, platform_name)

    @responses.activate
    def test_list_eggs(self):
        # Given
        python_tag = 'cp27'
        available_eggs = [
            ('nose', '1.3.0', '3', 'cp27'),
            ('numpy', '1.8.0', '1', 'py2')]
        platform_name = 'rh6-x86_64'
        self.brood_responses.test_list_eggs(
            available_eggs, python_tag, platform_name)

        platform = self.repository.platform(platform_name)

        # When
        metadata = platform.list_eggs(python_tag)

        # Then
        self.assertEqual(
            metadata, [{'name': 'nose-1.3.0-3.egg', 'python_tag': 'cp27'}])

    @responses.activate
    def test_egg_index(self):
        # Given
        python_tag = 'cp35'
        expected = {
            "numpy-1.11.3-3.egg": {
                u'available': True,
                u'build': 3,
                u'full_version': u'1.11.3-3',
                u'md5': u'95be1fd83e4d9b88aa1d3d6eb9d06d30',
                u'mtime': 1506778808.0,
                u'name': u'numpy',
                u'packages': [u'MKL 2017.0.3'],
                u'platform_abi': u'gnu',
                u'product': u'free',
                u'python_tag': python_tag,
                u'sha256': u'5a601cb05ae8b88f8675b8f5fe38f079b336a959bb3b927b9a14bac0027b45ee',
                u'size': 6671097,
                u'type': u'egg',
                u'version': u'1.11.3'}
        }

        platform_name = 'rh6-x86_64'
        self.brood_responses.test_egg_index(
            expected, python_tag, platform_name)
        platform = self.repository.platform(platform_name)

        # When
        metadata = platform.egg_index(python_tag)

        # Then
        self.assertEqual(metadata, expected)

    @responses.activate
    def test_get_egg_metadata(self):
        # Given
        python_tag = 'none'
        version = "1.2.6"
        full_version = version + '-3'
        expected = {
            "build": 3,
            "change_date": "2014-11-13T15:23:55.480886",
            "egg_basename": "zlib",
            "enabled": True,
            "filename": "zlib-1.2.6-3.egg",
            "full_version": full_version,
            "md5": "64314fe45217d65e36e308afcf0550f0",
            "name": "zlib",
            "packages": [],
            "platform_abi": "msvc2008",
            "product": "free",
            "python": None,
            "python_tag": 'none',
            "sha256": "babfd6f21dc6a2f4cc5a56860dbc407d7244168506c7d366d5cba1e07e2f09a8",
            "size": 69945,
            "type": "egg",
            "version": version}
        platform_name = 'win-x86'
        self.brood_responses.test_get_egg_metadata(expected, platform_name)
        platform = self.repository.platform(platform_name)

        # When
        metadata = platform.egg_metadata(python_tag, 'zlib', full_version)

        # Then
        self.assertEqual(metadata, expected)

    @responses.activate
    def test_download_egg(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_download_egg(platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        platform.download_egg(
            python_tag, name, full_version, destination=self.temp_dir)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertTrue(
            os.path.isfile(filename),
            msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_download_egg_provided_sha256(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_download_egg_provided_sha256(
            platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        platform.download_egg(
            python_tag, name, full_version, destination=self.temp_dir,
            expected_sha256=hashlib.sha256(body).hexdigest())

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertTrue(
            os.path.isfile(filename),
            msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_download_egg_provided_bad_sha256(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_download_egg_provided_bad_sha256(
            platform_name)
        name, full_version, python_tag, filename = values
        platform = self.repository.platform(platform_name)

        # When
        with self.assertRaises(ChecksumMismatchError):
            platform.download_egg(
                python_tag, name, full_version, destination=self.temp_dir,
                expected_sha256="78")

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertFalse(
            os.path.isfile(filename),
            msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

    @responses.activate
    def test_download_egg_filename_different_case(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_download_egg_filename_different_case(
            platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        platform.download_egg(
            python_tag, name, full_version, destination=self.temp_dir)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertTrue(os.path.isfile(filename),
                        msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_download_egg_invalid_sha(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_download_egg_invalid_sha(
            platform_name)
        name, full_version, python_tag, filename = values
        platform = self.repository.platform(platform_name)

        # When
        with self.assertRaises(ChecksumMismatchError):
            platform.download_egg(
                python_tag, name, full_version, destination=self.temp_dir)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

    @responses.activate
    def test_iter_download_egg(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_iter_download_egg(platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        length, iterator = platform.iter_download_egg(
            python_tag, name, full_version, destination=self.temp_dir)

        # Then
        self.assertEqual(length, len(body))
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(StopIteration):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertTrue(
            os.path.isfile(filename),
            msg='Expected file {0!r} to exist'.format(filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_iter_download_egg_bad_shasum(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_iter_download_egg_bad_shasum(platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        length, iterator = platform.iter_download_egg(
            python_tag, name, full_version, destination=self.temp_dir)

        # Then
        self.assertEqual(length, len(body))
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(ChecksumMismatchError):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist'.format(filename))

    @responses.activate
    def test_iter_download_egg_provided_sha256(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_iter_download_egg_provided_sha256(
            platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)
        sha256 = hashlib.sha256(body).hexdigest()
        content_length = len(body)

        # When
        length, iterator = platform.iter_download_egg(
            python_tag, name, full_version, destination=self.temp_dir,
            expected_sha256=sha256)

        # Then
        self.assertEqual(length, content_length)
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(StopIteration):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertTrue(
            os.path.isfile(filename),
            msg='Expected file {0!r} to exist'.format(filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_iter_download_egg_provided_bad_sha256(self):
        # Given
        platform_name = 'rh6-x86_64'
        values = self.brood_responses.test_iter_download_egg_provided_bad_sha256(
            platform_name)
        name, full_version, python_tag, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        length, iterator = platform.iter_download_egg(
            python_tag, name, full_version, destination=self.temp_dir,
            expected_sha256="35324513")

        # Then
        self.assertEqual(length, len(body))
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(ChecksumMismatchError):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist'.format(filename))

    @responses.activate
    def test_delete_egg(self):
        # Given
        name = 'numpy'
        version = '1.8.0-1'
        python_tag = 'py3'
        platform_name = 'rh5-64'
        self.brood_responses.test_delete_egg(
            name, version, python_tag, platform_name)
        platform = self.repository.platform(platform_name)

        # When
        platform.delete_egg(python_tag, name, version)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        self.assertEqual(request.method, "DELETE")

    @responses.activate
    def test_upload_egg(self):
        numpy = make_testing_egg(
            self.temp_dir, name=u'numpy', version=u'1.8.0', build=1)
        platform_name = numpy.platform
        self.brood_responses.test_upload_egg(platform_name)
        platform = self.repository.platform(platform_name)

        # When
        platform.upload_egg(numpy.path)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)

        self.assertJsonValid(json_data, 'upload_egg.json')
        self.assertRegexpMatches(request.url, r'^.*?\?.*?overwrite=False')
        self.assertRegexpMatches(request.url, r'^.*?\?.*?enabled=True')

    @responses.activate
    def test_upload_egg_unicode_filename(self):
        """
        Test for enthought/hatcher#113 to exhibit kennethreitz/requests#2411
        under Python 2.x.
        """
        # Given
        numpy = make_testing_egg(
            self.temp_dir, name=u'numpy', version=u'1.8.0', build=1)

        if not isinstance(numpy.path, six.text_type):
            numpy.path = numpy.path.decode('ascii')

        platform_name = numpy.platform
        self.brood_responses.test_upload_egg_unicode_filename(platform_name)
        platform = self.repository.platform(platform_name)

        # When
        platform.upload_egg(numpy.path)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)

        # Test for enthought/hatcher#113
        for line in request.body.splitlines():
            try:
                line = line.decode('utf-8')
            except UnicodeDecodeError:
                # We don't care about the binary data of the actual
                # file uploaded
                pass
            else:
                filename_match = BODY_FILENAME_RE.match(line)
                if filename_match is not None:
                    break
        else:
            self.fail('Unable to find filename in request body')
        self.assertEqual(
            filename_match.group(1), os.path.basename(numpy.filename))

        self.assertJsonValid(json_data, 'upload_egg.json')
        self.assertRegexpMatches(
            request.url, r'^.*?\?overwrite=False&enabled=True$')

    @responses.activate
    def test_upload_egg_force(self):
        # Given
        numpy = make_testing_egg(
            self.temp_dir, name=u'numpy', version=u'1.8.0', build=1)

        platform_name = numpy.platform
        platform = self.repository.platform(platform_name)
        self.brood_responses.test_upload_egg_force(platform_name)

        # When
        platform.upload_egg(numpy.path, overwrite=True)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_egg.json')
        self.assertRegexpMatches(
            request.url, r'^.*?\?overwrite=True&enabled=True$')

    @responses.activate
    def test_upload_egg_force_disabled(self):
        # Given
        numpy = make_testing_egg(
            self.temp_dir, name=u'numpy', version=u'1.8.0', build=1)

        platform_name = numpy.platform
        platform = self.repository.platform(platform_name)
        self.brood_responses.test_upload_egg_force_disabled(platform_name)

        # When
        platform.upload_egg(numpy.path, overwrite=True, enabled=False)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_egg.json')
        self.assertRegexpMatches(
            request.url, r'^.*?\?overwrite=True&enabled=False$')

    @responses.activate
    def test_upload_egg_disabled(self):
        # Given
        numpy = make_testing_egg(
            self.temp_dir, name=u'numpy', version=u'1.8.0', build=1)

        platform_name = numpy.platform
        platform = self.repository.platform(platform_name)
        self.brood_responses.test_upload_egg_disabled(platform_name)

        # When
        platform.upload_egg(numpy.path, enabled=False)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_egg.json')
        self.assertRegexpMatches(
            request.url, r'^.*?\?overwrite=False&enabled=False$')

    @responses.activate
    def test_list_runtimes(self):
        # Given
        expected = [
            'python_runtime_2.7.3_2.0.0.dev1-c9fa3fa_rh5-64_1.zip',
            'python_runtime_2.7.3_2.0.0.dev1-3fac9fa_rh5-64_2.zip']
        platform_name = 'rh5-64'
        self.brood_responses.test_list_runtimes()

        platform = self.repository.platform(platform_name)

        # When
        metadata = platform.list_runtimes()

        # Then
        six.assertCountEqual(self, metadata, expected)

    @responses.activate
    def test_runtime_index(self):
        # Given
        expected = {
            'python': {
                '2.7.3': {
                    '1': {
                        'build': 1,
                        'file_format': 'zip',
                        'filename': 'python_runtime_2.7.3_2.0.0.dev1-c9fa3fa_rh5-64_1.zip',  # noqa
                        'language': 'python',
                        'platform': 'rh5-64',
                        'sha256': '9713a9c3a35ab044133efa65233117eb11f2fabf413453dfc15dbc2dca23b858',  # noqa
                        "full_version": "2.7.3-1",
                        'version': '2.7.3'},
                    '2': {
                        'build': 2,
                        'file_format': 'zip',
                        'filename': 'python_runtime_2.7.3_2.0.0.dev1-3fac9fa_rh5-64_2.zip',  # noqa
                        'language': 'python',
                        'platform': 'rh5-64',
                        'sha256': 'eb11f2fabf413453dfc15dbc2dca23b8589713a9c3a35ab044133efa65233117',  # noqa
                        "full_version": "2.7.3-2",
                        'version': '2.7.3'}}}}
        platform_name = 'rh5-64'
        platform = self.repository.platform(platform_name)
        self.brood_responses.test_runtime_index(expected, platform_name)

        # When
        obtained_index = platform.runtime_index()

        # Then
        self.assertEqual(obtained_index, expected)

    @responses.activate
    def test_runtime_metadata(self):
        # Given
        language = 'python'
        python_tag = 'cp27'
        version = '2.7.3'
        build = 1
        full_version = '{0}-{1}'.format(version, build)
        platform_name = 'rh5-64'
        platform = self.repository.platform(platform_name)
        filename = 'python_runtime_2.7.3_2.0.0.dev1-c9fa3fa_win-32_1.zip'
        sha256 = "9713a9c3a35ab044133efa65233117eb11f2fabf413453dfc15dbc2dca23b858"  # noqa

        expected = {
            "build": build,
            "file_format": "zip",
            "filename": filename,
            "language": language,
            "platform": platform_name,
            "sha256": sha256,
            "full_version": full_version,
            "version": version,
        }
        self.brood_responses.test_runtime_metadata(
            python_tag, full_version, expected)

        # When
        metadata = platform.runtime_metadata(python_tag, full_version)

        # Then
        self.assertEqual(metadata, expected)

    @responses.activate
    def test_download_runtime(self):
        # Given
        values = self.brood_responses.test_download_runtime()
        python_tag, version, platform_name, body, filename = values
        platform = self.repository.platform(platform_name)

        # When
        platform.download_runtime(
            python_tag, version, destination=self.temp_dir)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertTrue(os.path.isfile(filename),
                        msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_download_runtime_bad_sha(self):
        # Given
        values = self.brood_responses.test_download_runtime_bad_sha()
        python_tag, version, platform_name, filename = values
        platform = self.repository.platform(platform_name)

        # When
        with self.assertRaises(ChecksumMismatchError):
            platform.download_runtime(
                python_tag, version, destination=self.temp_dir)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

    @responses.activate
    def test_download_runtime_provided_sha256(self):
        # Given
        values = self.brood_responses.test_download_runtime_provided_sha256()
        python_tag, version, platform_name, body, filename = values
        platform = self.repository.platform(platform_name)
        sha256 = hashlib.sha256(body).hexdigest()

        # When
        platform.download_runtime(
            python_tag, version, destination=self.temp_dir,
            expected_sha256=sha256)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertTrue(os.path.isfile(filename),
                        msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_download_runtime_provided_bad_sha256(self):
        # Given
        values = self.brood_responses.test_download_runtime_provided_bad_sha256()
        python_tag, version, platform_name, filename = values
        platform = self.repository.platform(platform_name)
        bad_body = 'not-data'.encode('ascii')
        sha256 = hashlib.sha256(bad_body).hexdigest()

        # When
        with self.assertRaises(ChecksumMismatchError):
            platform.download_runtime(
                python_tag, version, destination=self.temp_dir,
                expected_sha256=sha256)

        # Then
        filename = os.path.join(self.temp_dir, filename)
        temp_filename = '{0}.hatcher-partial'.format(filename)
        self.assertFalse(os.path.isfile(filename),
                         msg='Expected file {0!r} to exist'.format(filename))
        self.assertFalse(
            os.path.isfile(temp_filename),
            msg='Did not expect file {0!r} to exist yet'.format(temp_filename))

    @responses.activate
    def test_iter_download_runtime(self):
        # Given
        values = self.brood_responses.test_download_runtime()
        python_tag, version, platform_name, body, filename = values
        platform = self.repository.platform(platform_name)
        content_length = len(body)

        # When
        length, iterator = platform.iter_download_runtime(
            python_tag, version, destination=self.temp_dir)

        # Then
        self.assertEqual(length, content_length)
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

    @responses.activate
    def test_iter_download_runtime_bad_sha(self):
        # Given
        values = self.brood_responses.test_iter_download_runtime_bad_sha()
        python_tag, version, platform_name, body, filename = values
        platform = self.repository.platform(platform_name)
        content_length = len(body)

        # When
        length, iterator = platform.iter_download_runtime(
            python_tag, version, destination=self.temp_dir)

        # Then
        self.assertEqual(length, content_length),
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(ChecksumMismatchError):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist'.format(filename))

    @responses.activate
    def test_iter_download_runtime_provided_sha256(self):
        # Given
        values = self.brood_responses.test_iter_download_runtime_provided_sha256()
        python_tag, version, platform_name, body, filename = values
        platform = self.repository.platform(platform_name)
        sha256 = hashlib.sha256(body).hexdigest()
        content_length = len(body)

        # When
        length, iterator = platform.iter_download_runtime(
            python_tag, version, destination=self.temp_dir,
            expected_sha256=sha256)

        # Then
        self.assertEqual(length, content_length)
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(StopIteration):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertTrue(
            os.path.isfile(filename),
            msg='Expected file {0!r} to exist'.format(filename))

        with open(filename, 'rb') as fh:
            self.assertEqual(fh.read(), body)

    @responses.activate
    def test_iter_download_runtime_provided_bad_sha256(self):
        # Given
        values = self.brood_responses.test_iter_download_runtime_provided_bad_sha256()
        python_tag, version, platform_name, body, filename = values
        platform = self.repository.platform(platform_name)
        bad_body = 'not-data'.encode('ascii')
        sha256 = hashlib.sha256(bad_body).hexdigest()
        content_length = len(body)

        # When
        length, iterator = platform.iter_download_runtime(
            python_tag, version, destination=self.temp_dir,
            expected_sha256=sha256)

        # Then
        self.assertEqual(length, content_length)
        filename = os.path.join(self.temp_dir, filename)
        temp_filename_pattern = "{}*.hatcher-partial".format(
            os.path.join(self.temp_dir, os.path.basename(filename)))

        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))

        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 1,
            msg='Expected file {0!r} to exist'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist yet'.format(filename))

        with self.assertRaises(ChecksumMismatchError):
            next(iterator)
        tempfiles = glob.glob(temp_filename_pattern)

        self.assertEqual(
            len(tempfiles), 0,
            msg='Did not expect file {0!r} to exist yet'.format(tempfiles))
        self.assertFalse(
            os.path.isfile(filename),
            msg='Did not expect file {0!r} to exist'.format(filename))

    @responses.activate
    def test_upload_runtime(self):
        # Given
        filename = 'python_runtime_2.7.3_2.0.0.dev1-c9fa3fa_win-32_1.zip'
        data = 'python'
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as fh:
            fh.write(data)
        self.brood_responses.test_upload_runtime()

        # When
        self.repository.upload_runtime(filepath)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_runtime.json')
        self.assertRegexpMatches(request.url, r'^.*?\?overwrite=False$')

    @responses.activate
    def test_upload_runtime_force(self):
        # Given
        filename = 'python_runtime_2.7.3_2.0.0.dev1-c9fa3fa_win-32_1.zip'
        data = 'python'
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as fh:
            fh.write(data)
        self.brood_responses.test_upload_runtime()

        # When
        self.repository.upload_runtime(filepath, overwrite=True)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_runtime.json')
        self.assertRegexpMatches(request.url, r'^.*?\?overwrite=True$')

    @responses.activate
    def test_get_app_metadata(self):
        python_tag = 'cp27'
        version = '1.0'
        platform_name = 'rh5-64'
        app_id = 'mayavi'
        build = '1'
        expected = self.brood_responses.test_get_app_metadata(
            app_id, version, build, python_tag, platform_name)
        platform = self.repository.platform(platform_name)

        # When
        metadata = platform.app_metadata(
            python_tag, 'mayavi', version + '-' + build)

        # Then
        self.assertEqual(metadata, expected)

    @responses.activate
    def test_upload_app(self):
        # Given
        filename = 'mayavi.yaml'
        data = 'platform: "rh5-64"'
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as fh:
            fh.write(data)

        platform_name = 'rh5-64'
        self.brood_responses.test_upload_app(platform_name)

        # When
        self.repository.upload_app(filepath)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_app.json')
        self.assertRegexpMatches(request.url, r'^.*?\?overwrite=False$')

    @responses.activate
    def test_upload_app_force(self):
        # Given
        filename = 'mayavi.yaml'
        data = 'platform: "rh5-64"'
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as fh:
            fh.write(data)

        platform_name = 'rh5-64'
        self.brood_responses.test_upload_app_force(platform_name)

        # When
        self.repository.upload_app(filepath, overwrite=True)

        # Then
        self.assertEqual(len(responses.calls), 1)
        call, = responses.calls
        request, response = call
        json_data = self._parse_multipart_data(request.body, request.headers)
        self.assertJsonValid(json_data, 'upload_app.json')
        self.assertRegexpMatches(request.url, r'^.*?\?overwrite=True$')

    @responses.activate
    def test_list_apps(self):
        # Given
        expected = [
            ('mayavi.demo', '4.6.0-1', 'cp27'),
            ('numpy.demo', '1.0-1', 'cp27'),
            ('purepython', '1.0.0-2', 'py2')]

        platform_name = self.brood_responses.test_list_apps()

        platform = self.repository.platform(platform_name)

        # When
        metadata = platform.list_apps()

        # Then
        self.assertEqual(list(sorted(metadata)), list(sorted(expected)))

    @responses.activate
    def test_app_index(self):
        # Given
        given_index = {
            'numpy.demo': {
                '1.0': {
                    '1': {
                        'name': 'Numpy demo',
                        'description': 'Simple numpy demo',
                        'python_tag': 'cp27',
                    },
                },
            },
            'mayavi.demo': {
                '4.6': {
                    '1': {
                        'name': 'Mayavi demo',
                        'description': 'Simple mayavi demo',
                        'python_tag': 'cp27',
                    },
                },
            },
        }
        platform_name = 'rh5-64'
        self.brood_responses.test_app_index(given_index, platform_name)

        platform = self.repository.platform(platform_name)

        # When
        obtained_index = platform.app_index()

        # Then
        self.assertEqual(obtained_index, given_index)

    @responses.activate
    def test_reindex(self):
        # Given
        egg1 = make_testing_egg(self.temp_dir, name=u'egg1')
        duplicate_egg1 = make_testing_egg(self.temp_dir2, name=u'egg1')
        egg2 = make_testing_egg(self.temp_dir, name=u'egg2')
        egg3 = make_testing_egg(self.temp_dir, name=u'egg3', python_tag=None)
        eggs_to_enable = [egg1.path, duplicate_egg1.path, egg2.path, egg3.path]
        platform_name = egg1.platform

        def _eggs_entry(egg):
            return {
                'name': egg.name,
                'version': '{0}-{1}'.format(egg.version, egg.build),
                'python_tag': (egg.python_tag
                               if egg.python_tag is not None else 'none'),
            }

        expected = [
            _eggs_entry(egg1),
            _eggs_entry(egg2),
            _eggs_entry(egg3),
        ]

        json_str = self.brood_responses.test_reindex(platform_name)

        platform = self.repository.platform(platform_name)

        # When
        platform.reindex(eggs_to_enable)

        # Then
        self.assertJsonValid(json_str[0], 'enable_eggs_for_indexing.json')
        json_data = json.loads(json_str[0])
        self.assertEqual(list(json_data.keys()), ['eggs'])
        eggs = list(
            sorted(
                json_data['eggs'],
                key=lambda i: tuple(i.items())
            )
        )
        self.maxDiff = None
        self.assertEqual(eggs, expected)
