#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import json
import hashlib
import responses

from hatcher.core.url_templates import URLS_V1


class BroodResponses(object):
    """ Mocked brood responses for the repository tests.

    This class contains methods that will setup the necessary requests
    responses to mock the expected behaviour from brood. Each method
    is named after the related test in the related BaseTestRepository
    testcase for V1 entry points.

    """

    def __init__(self, url_handler, repository):
        self.url_handler = url_handler
        self.repository = repository
        self.urls = URLS_V1

    def response(self, path):
        handler = self.url_handler
        return '{scheme}://{host}{path}'.format(
            scheme=handler.scheme, host=handler.host, path=path)

    def dummy_index_egg_metadata(self, name, version, build, python_tag):
        # Note: We do not define sha256 and md5
        return {
            u'available': True,
            u'build': build,
            u'full_version': '{}-{}'.format(version, build),
            u'mtime': 1506778808.0,
            u'name': name,
            u'packages': [],
            u'platform_abi': u'gnu',
            u'product': u'free',
            u'python_tag': python_tag,
            u'size': 6671097,
            u'type': u'egg',
            u'version': version}

    def dummy_egg_metadata(self, body):
        return {
            "build": 3,
            "change_date": "2014-11-13T15:08:04.412025",
            "egg_basename": "numpy",
            "enabled": True,
            "filename": "numpy-1.11.3-3.egg",
            "full_version": "1.11.3",
            "name": "numpy",
            "packages": [],
            "platform_abi": "msvc2008",
            "product": "free",
            "python": None,
            "python_tag": "cp35",
            "sha256": hashlib.sha256(body).hexdigest(),
            "md5": hashlib.md5(body).hexdigest(),
            "size": len(body),
            "type": "egg",
            "version": "1.11.3"}

    def dummy_runtime_metadata(self, body):
        return {
            "abi": "gnu",
            "build_revision": "2e27fc462cb45fd6cbce0000b62e2d89923e2449",
            "filename": "cpython-2.7.10+2-rh5_x86_64-gnu.runtime",
            "implementation": "cpython",
            "language_version": "2.7.10",
            "metadata_version": "1.0",
            "platform": 'rh5-x86_64',
            "sha256": hashlib.sha256(body).hexdigest(),
            "version": '2.7.10+2'}

    def runtime_download_response(self, metadata, body):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.data.runtimes.download.format(
                    organization_name='enthought',
                    repository_name='free',
                    platform=metadata['platform'],
                    implementation=metadata['implementation'],
                    version=metadata['version'])),
            body=body,
            status=200,
            content_type='application/octet-stream',
            adding_headers={
                'Content-Length': str(len(body)),
                'Content-Disposition': 'attachment; filename="{0}"'.format(
                    metadata['filename'])})

    def runtime_metadata_response(self, metadata):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.metadata.artefacts.runtimes.format(
                    organization_name='enthought',
                    repository_name='free',
                    platform=metadata['platform'],
                    implementation=metadata['implementation'],
                    version=metadata['version'])),
            body=json.dumps(metadata),
            status=200,
            content_type='application/json')

    def egg_download_response(self, metadata, body, platform):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.data.eggs.download.format(
                    organization_name='enthought',
                    repository_name='free',
                    platform=platform,
                    name=metadata['name'],
                    python_tag=metadata['python_tag'],
                    version=metadata['version'])),
            body=body,
            status=200,
            content_type='application/octet-stream',
            adding_headers={
                'Content-Length': str(len(body)),
                'Content-Disposition': 'attachment; filename="{0}"'.format(
                    metadata['filename'])})

    def egg_metadata_response(self, metadata, platform):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.metadata.artefacts.eggs.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform,
                    python_tag=metadata['python_tag'],
                    name=metadata['name'],
                    version=metadata['full_version'])),
            body=json.dumps(metadata),
            status=200,
            content_type='application/json')

    def test_delete_repository(self):
        responses.add(
            responses.DELETE,
            self.response(
                self.urls.admin.repositories.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name)))

    def test_delete_repository_force(self):
        responses.add(
            responses.DELETE,
            self.response(
                path=self.urls.admin.repositories.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name)))

    def test_get_metadata(self, expected):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.admin.repositories.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name)),
            body=json.dumps(expected),
            status=200,
            content_type='application/json')

    def test_list_platforms(self, expected):
        responses.add(
            self.response(
                path=self.urls.admin.repositories.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name)),
            body=json.dumps({'platforms': expected}),
            status=200,
            content_type='application/json')

    def test_list_eggs(self, available, python_tag, platform_name):
        index = {
            '{}-{}-{}.egg'.format(name, version, build, tag):
            self.dummy_index_egg_metadata(name, version, build, tag)
            for name, version, build, tag in available
            if tag == python_tag}
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.indices.eggs.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name,
                    python_tag=python_tag)),
            body=json.dumps(index),
            status=200,
            content_type='application/json')

    def test_egg_index(self, expected, python_tag, platform_name):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.indices.eggs.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name,
                    python_tag=python_tag)),
            body=json.dumps(expected),
            status=200,
            content_type='application/json')

    def test_get_egg_metadata(self, expected, platform):
        self.egg_metadata_response(expected, platform)

    def test_download_egg(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        self.egg_metadata_response(metadata, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_download_egg_provided_sha256(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_download_egg_provided_bad_sha256(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], metadata['filename'])

    def test_download_egg_filename_different_case(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        self.egg_metadata_response(metadata, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_download_egg_invalid_sha(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        metadata['sha256'] = "sfsdgfsdgadg3"
        self.egg_download_response(metadata, body, platform)
        self.egg_metadata_response(metadata, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], metadata['filename'])

    def test_iter_download_egg(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        self.egg_metadata_response(metadata, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_iter_download_egg_bad_shasum(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        metadata['sha256'] = "sfsdgfsdgadg3"
        self.egg_download_response(metadata, body, platform)
        self.egg_metadata_response(metadata, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_iter_download_egg_provided_sha256(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_iter_download_egg_provided_bad_sha256(self, platform):
        body = 'data'.encode('ascii')
        metadata = self.dummy_egg_metadata(body)
        self.egg_download_response(metadata, body, platform)
        return (
            metadata['name'], metadata['full_version'],
            metadata['python_tag'], body, metadata['filename'])

    def test_delete_egg(self, name, version, python_tag, platform_name):
        responses.add(
            responses.DELETE,
            self.response(
                path=self.urls.data.eggs.delete.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name,
                    name=name,
                    version=version,
                    python_tag=python_tag)))

    def test_upload_egg(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.eggs.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)))

    def test_upload_egg_unicode_filename(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.eggs.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)))

    def test_upload_egg_force(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.eggs.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)))

    def test_upload_egg_force_disabled(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.eggs.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)))

    def test_upload_egg_disabled(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.eggs.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)))

    def test_list_runtimes(self):
        index = {
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
                    "version": "3.4.3+2"}}}
        platform_name = 'rh5-x86_64'
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.indices.runtimes.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)),
            body=json.dumps(index),
            status=200,
            content_type='application/json')

    def test_runtime_index(self, index, platform_name):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.indices.runtimes.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)),
            body=json.dumps(index),
            status=200,
            content_type='application/json')

    def test_runtime_metadata(self, expected):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.metadata.artefacts.runtimes.format(
                    organization_name='enthought',
                    repository_name='free',
                    platform=expected['platform'],
                    implementation=expected['implementation'],
                    version=expected['version'])),
            body=json.dumps(expected),
            status=200,
            content_type='application/json')

    def test_download_runtime(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        self.runtime_download_response(metadata, body)
        self.runtime_metadata_response(metadata)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], body, metadata['filename'])

    def test_download_runtime_bad_sha(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        metadata["sha256"] = "2141235sss"
        self.runtime_download_response(metadata, body)
        self.runtime_metadata_response(metadata)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], metadata['filename'])

    def test_download_runtime_provided_sha256(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        self.runtime_download_response(metadata, body)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], body, metadata['filename'])

    def test_download_runtime_provided_bad_sha256(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        self.runtime_download_response(metadata, body)
        self.runtime_metadata_response(metadata)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], metadata['filename'])

    def test_iter_download_runtime(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        self.runtime_download_response(metadata, body)
        self.runtime_metadata_response(metadata)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], body, metadata['filename'])

    def test_iter_download_runtime_bad_sha(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        metadata["sha256"] = "2141235sss"
        self.runtime_download_response(metadata, body)
        self.runtime_metadata_response(metadata)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], body, metadata['filename'])

    def test_iter_download_runtime_provided_sha256(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        self.runtime_download_response(metadata, body)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], body, metadata['filename'])

    def test_iter_download_runtime_provided_bad_sha256(self):
        body = 'data'.encode('ascii')
        metadata = self.dummy_runtime_metadata(body)
        self.runtime_download_response(metadata, body)
        return (
            metadata['implementation'], metadata['version'],
            metadata['platform'], body, metadata['filename'])

    def test_upload_runtime(self, platform):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.runtimes.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform)))

    def test_upload_runtime_force(self, platform):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.runtimes.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform)))

    def test_get_app_metadata(
            self, app_id, version, build, python_tag, platform_name):
        expected = {
            'id': app_id,
            'version': version,
            'other_key': 'value',
            'python_tag': python_tag}
        responses.add(
            responses.GET,
            '{scheme}://{host}{path}'.format(
                scheme=self.url_handler.scheme,
                host=self.url_handler.host,
                path=self.urls.metadata.artefacts.apps.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name,
                    python_tag=python_tag,
                    app_id=app_id,
                    version=version + '-' + build)),
            body=json.dumps(expected),
            status=200,
            content_type='application/json')
        return expected

    def test_upload_app(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.apps.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name,
                ),
            ),
        )

    def test_upload_app_force(self, platform_name):
        responses.add(
            responses.POST,
            self.response(
                path=self.urls.data.apps.upload.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)))

    def test_list_apps(self):
        platform = 'rh5-64'
        given_index = {
            'cp27': {
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
                    '4.6.0': {
                        '1': {
                            'name': 'Mayavi demo',
                            'description': 'Simple mayavi demo',
                            'python_tag': 'cp27',
                        },
                    },
                },
            },
            'py2': {
                'purepython': {
                    '1.0.0': {
                        '2': {
                            'name': 'Pure Python',
                            'description': 'None',
                            'python_tag': 'py2',
                        },
                    },
                },
            },
        }

        responses.add(
            responses.GET,
            self.response(
                path=self.urls.indices.apps.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform)),
            body=json.dumps(given_index),
            status=200,
            content_type='application/json')
        return platform

    def test_app_index(self, given_index, platform_name):
        responses.add(
            responses.GET,
            self.response(
                path=self.urls.indices.apps.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)),
            body=json.dumps(given_index),
            status=200,
            content_type='application/json')

    def test_reindex(self, platform_name):
        json_str = [None]

        def callback(request):
            json_str[0] = request.body
            return (202, {}, '')

        responses.add_callback(
            responses.POST,
            self.response(
                path=self.urls.data.eggs.re_index.format(
                    organization_name=self.repository.organization_name,
                    repository_name=self.repository.name,
                    platform=platform_name)),
            callback=callback)
        return json_str
