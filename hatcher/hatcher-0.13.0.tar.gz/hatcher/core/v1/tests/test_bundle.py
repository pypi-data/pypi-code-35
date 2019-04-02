#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
""" Test bundle controllers."""

from __future__ import absolute_import, print_function, unicode_literals

import json
import os
from hashlib import sha256
from os import path
from shutil import rmtree
from tempfile import mkdtemp
import unittest

import responses

from hatcher.core.brood_url_handler import BroodURLHandler
from hatcher.core.model_registry import ModelRegistry
from hatcher.core.tests.common import JsonSchemaTestMixin
from hatcher.core.url_templates import URLS_V1
from hatcher.core.utils import python_tag
from hatcher.core.v1.bundle import (
    BundleCollectionController,
    BundleControllerFactory,
    BundleResourceFileController,
    BundleResourceController
)
from hatcher.core.v1.repository import Repository, SinglePlatformRepository
from hatcher.errors import TargetFileExists
from hatcher.tests.common import patch


HASH_FUNC = sha256

BUNDLE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data/example_bundle-1.0.0-1.bundle',
)

DEFAULT_BUNDLE_DATA = {
    "modifiers": {
        "allow_newer": [],
        "allow_any": [],
        "allow_older": []
    },
    "requirements": [
        {
            "sha256": "f9b9b4c5925c5d14f322dd2e67ca6fdcd482d11efd298dc0d74a0a96df17fde7",  # noqa
            "version": "9.0.1-1",
            "name": "pip",
            "repository": "enthought/free"
        },
        {
            "sha256": "c982237f95eed2126c99b07a67e1c82449548f9dbe5203d216b1f692bee832eb",  # noqa
            "version": "1.10.0-1",
            "name": "six",
            "repository": "enthought/free"
        }
    ],
    "metadata_version": "2.0",
    "repositories": {
        "packages": [
            "enthought/free",
            "enthought/gpl"
        ],
        "runtimes": [
            "enthought/free"
        ]
    },
    "mark": [
        {
            "state": "manual",
            "name": "pip"
        },
        {
            "state": "auto",
            "name": "six"
        }
    ],
    "runtime": {
        "repository": "enthought/free",
        "implementation": "cpython",
        "platform": "rh5_x86_64",
        "version": "3.6.0+3",
        "platform_abi": "gnu",
        "sha256": "7d367673aa2c070f726f43819b9fbb89aacba1fab74224831bbc1bd44c1bd33d"  # noqa
    }
}


class BundleInfo(object):
    """ Define test info for the bundle."""

    def __init__(self, organization='org', repository='repo', platform='plat',
                 python_tag='cp36', name='bundle', version='1.0.0-1',
                 data=DEFAULT_BUNDLE_DATA):
        """Instantiate a bundle with ``kwargs`` or defaults."""
        self.data = data
        self.name = name
        self.organization = organization
        self.platform = platform
        self.python_tag = python_tag
        self.repository = repository
        self.version = version


class BundleURLs(object):
    """ Expected URLs for the bundle described by ``BundleInfo``.

    This is separated out in order to more easily update tests when
    hatcher is no longer the source of truth for its URLs.
    """
    _root = '/api/v1/json'
    _mid = 'org/repo/plat/bundles'
    _tail = 'cp36/bundle/1.0.0-1'

    index = '{}/indices/{}'.format(_root, _mid)
    metadata = '{}/metadata/{}/{}'.format(_root, _mid, _tail)
    upload = '{}/data/org/repo/bundles/upload'.format(_root)


def expected_index_metadata(bundle):
    """ Return the expected index response for a provided bundle."""
    return {
        'build': bundle.version.split('-')[1],
        'full_version': bundle.version,
        'name': bundle.name,
        'platform': bundle.collection.platform.name,
        'python_tag': bundle.python_tag,
        'version': bundle.version.split('-')[0],
    }


def expected_metadata(bundle):
    """ Return expected metadata for the provided bundle.

    .. note::
        The "real" metadata object returned from the server also has
        a ``data`` key, which contains the unparsed bundle JSON. It
        is not included here for simplicity's sake.

    Parameters
    ----------
    bundle : BundleResourceController
        a BundleInfo object

    Returns
    -------
    dict
        the bundle metadata
    """
    metadata = expected_index(bundle)
    metadata['data'] = getattr(
        getattr(bundle, '_info', object),
        'data',
        DEFAULT_BUNDLE_DATA,
    )
    return metadata


def expected_index(*bundles):
    """ Return the expected index for the provided bundles.

    Parameters
    ----------
    *bundles : BundleResourceController
        bundles that should be included in the index.
    """
    index = {}
    for bundle in bundles:
        index.setdefault(bundle.python_tag, {})
        python_tag = index[bundle.python_tag]

        python_tag.setdefault(bundle.name, {})
        name = python_tag[bundle.name]

        version, build = bundle.version.split('-')

        name.setdefault(version, {})
        version = name[version]

        version[build] = expected_index_metadata(bundle)

    return index


def expected_list(*bundles):
    return [
        {
            'python_tag': b.python_tag,
            'name': b.name,
            'version': b.version
        } for b in bundles
    ]


def url_handler_factory():
    return BroodURLHandler.from_auth('http://brood-dev')


def repository_factory(url_handler_factory_=url_handler_factory):
    bundle = BundleInfo()
    return Repository(
        organization_name=bundle.organization,
        name=bundle.repository,
        url_handler=url_handler_factory_(),
        model_registry=ModelRegistry(api_version=1)
    )


def platform_factory(repository_factory_=repository_factory):
    repo = repository_factory_()
    bundle = BundleInfo()
    return SinglePlatformRepository(
        repository=repo,
        platform=bundle.platform,
        url_handler=repo._url_handler,
        model_registry=repo._model_registry
    )


def bundle_collection_factory(platform_factory_=platform_factory):
    return BundleCollectionController(
        platform=platform_factory_(), url_template=URLS_V1
    )


def bundle_controller_factory_factory(repository_factory_=repository_factory):
    return BundleControllerFactory(
        repository=repository_factory_(),
        url_template=URLS_V1
    )


def bundle_resource_factory(
        bundle_collection_factory_=bundle_collection_factory,
        bundle_info=BundleInfo()):
    bundle = BundleResourceController(
        collection=bundle_collection_factory_(),
        python_tag=bundle_info.python_tag,
        name=bundle_info.name,
        version=bundle_info.version
    )
    bundle._info = bundle_info
    return bundle


def bundlefile_bundle_info(filepath, **kwargs):
    """Return bundle information for the specified bundle file.

    **kwargs are passed directly to BundleInfo()
    """
    with open(filepath) as bundlefile:
        data = json.load(bundlefile)
    return BundleInfo(data=data, **kwargs)


def default_bundlefile_info(**kwargs):
    """Return expected bundle information for the file at BUNDLE_PATH."""
    bundle_kwargs = {
        'name': 'example_bundle',
        'version': '1.0.0-1',
        'python_tag': 'cp27'
    }
    bundle_kwargs.update(**kwargs)
    return bundlefile_bundle_info(
        BUNDLE_PATH,
        **bundle_kwargs
    )


def bundle_file_resource_factory():
    return bundle_controller_factory_factory().from_file(BUNDLE_PATH)


def bundle_file_dict(bundle_path=BUNDLE_PATH):
    with open(bundle_path) as bfile:
        return json.load(bfile)


def bundle_file_runtime_dict(bundle_path=BUNDLE_PATH):
    return bundle_file_dict(bundle_path)['runtime']


def response_path(url_handler, path):
    """ Return the full URL for the given path.

    Parameters
    ----------
    url_handler : hatcher.core.brood_url_handler.BroodURLHandler
        a URL handler instance
    path : str
        the URL path

    Returns
    -------
    str
        The full URL path
    """
    return '{}://{}{}'.format(url_handler.scheme, url_handler.host, path)


def add_json_response(rsps, method, bundle, path, data, status):
    """ Add a JSON response to the responses object.

    Parameters
    ----------
    rsps : responses.RequestMock
        request mock instance
    method : str
        request method string (capitalized), e.g. "GET"
    bundle: BundleResourceController or BundleCollectionController
        the bundle for which the request is being generated
    path : str
        the path portion of the URL
    data: dict
        data to return as JSON
    status : int
        HTTP status code
    """
    rsps.add(
        method,
        response_path(bundle.url_handler, path),
        json=data,
        status=status,
        content_type='application/json',
    )


def add_json_bundle_index_response(rsps, collection, *bundles):
    """ Add a standard index GET success response.

    Parameters
    ----------
    rsps : responses.RequestMock
        request mock instance
    *bundles: BundleResourceController or BundleCollectionController
        bundles to add to the index
    """
    add_json_response(
        rsps,
        method=rsps.GET,
        bundle=collection,
        path=collection.index_path,
        data=expected_index(*bundles),
        status=200,
    )


def add_json_bundle_metadata_response(rsps, bundle):
    """ Add a standard metadata GET success response.

    Parameters
    ----------
    rsps : responses.RequestMock
        request mock instance
    bundle: BundleResourceController or BundleCollectionController
        the bundle for which the request is being generated
    """
    add_json_response(
        rsps,
        method=rsps.GET,
        bundle=bundle,
        path=bundle.metadata_path,
        data=expected_metadata(bundle),
        status=200,
    )


def add_upload_bundle_response(rsps, bundle):
    """ Add a standard upload response for the specified bundle."""
    rsps.add(
        rsps.POST,
        response_path(bundle.url_handler, bundle.upload_path),
    )


def assert_valid_bundle_upload(tc, rsps, overwrite=False):
    """ Check the bundle upload request is properly formed.

    Parameters
    ----------
    tc : unittest.TestCase
        a TestCase instance with the JsonSchemaTestMixin mixed in
    rsps : responses.RequestsMock
        a requests mock instance used to perform an upload request
    overwrite : bool
        whether the request was made with overwrite True or False
    """
    tc.assertTrue(len(rsps.calls) == 1)
    request = rsps.calls[0][0]
    tc.assertJsonValid(
        tc._parse_multipart_data(request.body, request.headers),
        'edm_bundle_v2.json'
    )
    if overwrite:
        tc.assertTrue('overwrite=True' in request.url)
    else:
        tc.assertTrue('overwrite=False' in request.url)


class TestBundleResource(unittest.TestCase):
    """ Unit tests for the bundle resource."""

    # ------------------------------------------------------------------
    # Local Operations
    # ------------------------------------------------------------------

    def test_metadata_path(self):
        bundle = bundle_resource_factory()
        self.assertEqual(bundle.metadata_path, BundleURLs.metadata)

    def test_upload_path(self):
        bundles = bundle_resource_factory()
        self.assertEqual(bundles.upload_path, BundleURLs.upload)

    def test_lazy_dict(self):
        bundle = bundle_resource_factory()
        exp_bundle_info = BundleInfo()
        exp = {
            'python_tag': exp_bundle_info.python_tag,
            'name': exp_bundle_info.name,
            'version': exp_bundle_info.version,
        }
        self.assertEqual(bundle.lazy_dict, exp)

    def test_canonical_filename(self):
        """Test automatic determination of bundle filename."""
        bundle_info = BundleInfo()
        bundle = bundle_resource_factory(bundle_info=bundle_info)
        exp = '{}-{}.{}'.format(
            bundle_info.name,
            bundle_info.version,
            BundleResourceController.BUNDLE_EXTENSION
        )
        self.assertEqual(bundle.canonical_filename, exp)

    def test_filename_regex(self):
        """ Test the regex used to parse filenames."""
        for filename, exp_groups in (
            ('foo-1.0.0-1.bundle', ('foo', '1.0.0', '1')),
            ('foo-18.1-1.bundle', ('foo', '18.1', '1')),
            ('foo-1001-1.bundle', ('foo', '1001', '1')),
            ('foo-1.0.0.dev10-1.bundle', ('foo', '1.0.0.dev10', '1')),
            ('foo-1.0.0rc1-1.bundle', ('foo', '1.0.0rc1', '1')),
            ('foo-1.0.0-11234.bundle', ('foo', '1.0.0', '11234')),
            ('up_down-3.1.2-3.bundle', ('up_down', '3.1.2', '3')),
            (
                'my_great_bundle-1.0.0-1.bundle',
                ('my_great_bundle', '1.0.0', '1')
            ),
        ):
            match = BundleResourceController.BUNDLE_RE.match(filename)
            self.assertEqual(exp_groups, match.groups())

    def test_filename_regex_bad_names(self):
        """ Test the regex on improper names."""
        for filename in (
            'foo-bar-baz-1.0.0.bundle',
            'foo-bar-1.0.0-1.bundle',
            'foo-1.0.0-1-2.bundle',
            'foobar-1.0.0.bundle',
            'a_b_c-1.0.0.bundle',
            'a_b_c.bundle',
            'my-cool-bundle.bundle',
            'my-cool-bundle-1.bundle',
        ):
            self.assertIsNone(
                BundleResourceController.BUNDLE_RE.match(filename)
            )

    def test_equality(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        self.assertTrue(b_one is not b_two)
        self.assertTrue(b_one == b_two)

    def test_inequality_org_name(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        b_two.collection.platform._repository.organization_name = 'other'
        self.assertTrue(b_one != b_two)

    def test_inequality_repo_name(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        b_two.collection.platform._repository.name = 'other'
        self.assertTrue(b_one != b_two)

    def test_inequality_platform_name(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        b_two.collection.platform.name = 'other'
        self.assertTrue(b_one != b_two)

    def test_inequality_python_tag(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        b_two.python_tag = 'other'
        self.assertTrue(b_one != b_two)

    def test_inequality_name(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        b_two.name = 'other'
        self.assertTrue(b_one != b_two)

    def test_inequality_version(self):
        b_one, b_two = bundle_resource_factory(), bundle_resource_factory()
        b_two.version = 'other'
        self.assertTrue(b_one != b_two)

    def test_str_does_not_error(self):
        str(bundle_resource_factory())

    def test_repr_does_not_error(self):
        repr(bundle_resource_factory())

    # ------------------------------------------------------------------
    # Remote Operations
    # ------------------------------------------------------------------

    def test_metadata(self):
        bundle = bundle_resource_factory()
        with responses.RequestsMock() as rsps:
            add_json_bundle_metadata_response(rsps, bundle)
            self.assertEqual(bundle.metadata(), expected_metadata(bundle))

    def test_save(self):
        """Test saving a bundlefile."""
        bundle = bundle_resource_factory()
        coll = bundle_collection_factory()
        tmpdir = mkdtemp()

        try:
            with responses.RequestsMock() as rsps:
                add_json_bundle_metadata_response(rsps, bundle)
                filepath = bundle.save(tmpdir)
            self.assertTrue(filepath.endswith(bundle.canonical_filename))
            bundle_from_file = coll.from_file(filepath)
            self.assertEqual(bundle, bundle_from_file)
        finally:
            rmtree(tmpdir)

    def test_save_exists(self):
        """Test saving when the target already exists."""
        bundle = bundle_resource_factory()
        tmpdir = mkdtemp()
        exp_path = path.join(tmpdir, bundle.canonical_filename)
        with open(exp_path, 'w') as fp:
            fp.write('foo')

        try:
            with self.assertRaises(TargetFileExists):
                bundle.save(tmpdir)
        finally:
            rmtree(tmpdir)

    def test_save_exists_overwrite(self):
        """Test that we can overwrite an existing file if asked."""
        bundle = bundle_resource_factory()
        coll = bundle_collection_factory()
        tmpdir = mkdtemp()
        exp_path = path.join(tmpdir, bundle.canonical_filename)
        with open(exp_path, 'w') as fp:
            fp.write('foo')

        try:
            with responses.RequestsMock() as rsps:
                add_json_bundle_metadata_response(rsps, bundle)
                bundle.save(tmpdir, overwrite=True)
            with open(exp_path) as fp:
                bundle_from_file = coll.from_file(exp_path)
            self.assertEqual(bundle, bundle_from_file)
        finally:
            rmtree(tmpdir)


class TestBundleFileResourceController(JsonSchemaTestMixin, unittest.TestCase):
    """ Unit tests for the file resource controller."""

    def test_repr_no_error(self):
        repr(bundle_file_resource_factory())

    def test_equality(self):
        self.assertTrue(
            bundle_file_resource_factory() == bundle_file_resource_factory()
        )

    def test_inequality_filename(self):
        one = bundle_file_resource_factory()
        two = bundle_file_resource_factory()
        two.filepath = 'other'
        self.assertTrue(one != two)

    def test_access_bundle_resources(self):
        bundle = bundle_file_resource_factory()
        attrs = (
            'collection',
            'python_tag',
            'name',
            'version',
            'url_handler',
        )
        for attr in attrs:
            assert getattr(bundle, attr) is getattr(bundle.bundle, attr)

    def test_upload(self):
        bundle = bundle_file_resource_factory()
        with responses.RequestsMock() as rsps:
            add_upload_bundle_response(rsps, bundle)
            bundle.upload()
            assert_valid_bundle_upload(self, rsps, overwrite=False)

    def test_upload_overwrite(self):
        bundle = bundle_file_resource_factory()
        overwrite = True
        with responses.RequestsMock() as rsps:
            add_upload_bundle_response(rsps, bundle)
            bundle.upload(overwrite=overwrite)
            assert_valid_bundle_upload(self, rsps, overwrite=overwrite)


class TestBundleCollection(unittest.TestCase):
    """ Unit tests for the bundle collection."""

    # ------------------------------------------------------------------
    # Local Operations
    # ------------------------------------------------------------------

    def test_index_path(self):
        bundles = bundle_collection_factory()
        self.assertEqual(bundles.index_path, BundleURLs.index)

    def test_from_file(self):
        """Test retrieving bundle information from a file."""
        bundles = bundle_collection_factory()
        exp_info = default_bundlefile_info()
        bundle = bundles.from_file(BUNDLE_PATH)
        self.assertEqual(bundle.name, exp_info.name)
        self.assertEqual(bundle.version, exp_info.version)
        self.assertEqual(bundle.python_tag, exp_info.python_tag)

    def test_from_file_runtime_provided(self):
        """Test parsing bundle information when a runtime is provided."""
        bundles = bundle_collection_factory()
        exp_info = default_bundlefile_info(python_tag='cp36')
        with patch.object(bundles, '_runtime_dict_from_bundle_file') as meth:
            bundle = bundles.from_file(
                BUNDLE_PATH,
                runtime={
                    'implementation': 'cpython',
                    'version': '3.6.13+3',
                }
            )
            meth.assert_not_called()
        self.assertEqual(bundle.name, exp_info.name)
        self.assertEqual(bundle.version, exp_info.version)
        self.assertEqual(bundle.python_tag, 'cp36')

    def test_get(self):
        bundles = bundle_collection_factory()
        exp_bundle = bundle_resource_factory()
        bundle_info = BundleInfo()
        res_bundle = bundles.get(
            bundle_info.python_tag, bundle_info.name, bundle_info.version
        )
        self.assertTrue(exp_bundle == res_bundle)

    def test_str_does_not_error(self):
        str(bundle_collection_factory())

    def test_repr_does_not_error(self):
        repr(bundle_collection_factory())

    # ------------------------------------------------------------------
    # Remote Operations
    # ------------------------------------------------------------------

    def test_index(self):
        collection = bundle_collection_factory()
        bundle_two_info = BundleInfo(version='1.0.0-2')
        bundle_three_info = BundleInfo(version='1.1.0-1')

        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(bundle_info=bundle_two_info),
            bundle_resource_factory(bundle_info=bundle_three_info)
        )

        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, collection, *bundles)
            self.assertEqual(expected_index(*bundles), collection.index())

    def test_list_multi_version(self):
        collection = bundle_collection_factory()
        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(bundle_info=BundleInfo(version='1.0.0-2')),
            bundle_resource_factory(bundle_info=BundleInfo(version='1.1.0-1')),
        )

        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, collection, *bundles)
            lst = collection.list()

        self.assertEqual(len(bundles), len(lst))
        # order not guaranteed, so sort them first.
        self.assertEqual(
            sorted(expected_list(*bundles), key=lambda d: d['version']),
            sorted(lst, key=lambda d: d['version'])
        )
        assert all(
            b.version in (l['version'] for l in lst) for b in bundles
        )

    def test_list_multi_name(self):
        collection = bundle_collection_factory()
        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(bundle_info=BundleInfo(name='barpak')),
            bundle_resource_factory(bundle_info=BundleInfo(name='bazpak')),
        )

        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, collection, *bundles)
            lst = collection.list()

        self.assertEqual(len(bundles), len(lst))
        # order not guaranteed, so sort them first.
        self.assertEqual(
            sorted(expected_list(*bundles), key=lambda d: d['name']),
            sorted(lst, key=lambda d: d['name'])
        )
        assert all(
            b.name in (l['name'] for l in lst) for b in bundles
        )

    def test_list_multi_python_tag(self):
        collection = bundle_collection_factory()

        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(bundle_info=BundleInfo(python_tag='cp27')),
            bundle_resource_factory(bundle_info=BundleInfo(python_tag='cp34')),
        )

        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, collection, *bundles)
            lst = collection.list()

        self.assertEqual(len(bundles), len(lst))
        # order not guaranteed, so sort them first.
        self.assertEqual(
            sorted(expected_list(*bundles), key=lambda d: d['python_tag']),
            sorted(lst, key=lambda d: d['python_tag'])
        )
        assert all(
            b.python_tag in (l['python_tag'] for l in lst) for b in bundles
        )

    def test_iter(self):
        collection = bundle_collection_factory()
        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(bundle_info=BundleInfo(version='1.0.0-2')),
            bundle_resource_factory(bundle_info=BundleInfo(version='1.1.0-1'))
        )

        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, collection, *bundles)
            # The explicit call to iter() validates we can make an iterable.
            coll_iter = iter(collection)
            resources = list(coll_iter)

        for bundle in bundles:
            assert bundle in resources


class TestBundleFactory(unittest.TestCase):
    """ Test the bundle maker."""

    def test_from_file(self):
        factory = bundle_controller_factory_factory()
        exp_info = default_bundlefile_info()

        bundle = factory.from_file(BUNDLE_PATH)
        file_dict = bundle_file_dict()

        runtime = file_dict['runtime']
        exp_py_tag = python_tag(runtime['implementation'], runtime['version'])

        self.assertTrue(isinstance(bundle, BundleResourceFileController))
        self.assertEqual(bundle.collection.platform.name, runtime['platform'])
        self.assertEqual(bundle.python_tag, exp_py_tag)
        self.assertEqual(bundle.name, exp_info.name)
        self.assertEqual(bundle.version, exp_info.version)
        self.assertEqual(bundle.filepath, BUNDLE_PATH)

    def test_from_runtime_dict(self):
        factory = bundle_controller_factory_factory()
        runtime = bundle_file_runtime_dict()
        bundle_info = BundleInfo()
        bundle = factory.from_runtime_dict(
            runtime, bundle_info.name, bundle_info.version
        )
        exp_py_tag = python_tag(runtime['implementation'], runtime['version'])

        self.assertEqual(bundle.collection.platform.name, runtime['platform'])
        self.assertEqual(bundle.python_tag, exp_py_tag)
        self.assertEqual(bundle_info.name, bundle.name)
        self.assertEqual(bundle_info.version, bundle.version)


class TestBundleIntegration(JsonSchemaTestMixin, unittest.TestCase):

    def test_bundles_attribute(self):
        self.assertTrue(
            isinstance(platform_factory().bundles, BundleCollectionController)
        )

    def test_bundle_index(self):
        platform = platform_factory()
        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(
                bundle_info=BundleInfo(version='1.1.0-1')
            ),
            bundle_resource_factory(
                bundle_info=BundleInfo(version='1.2.0-1')
            ),
        )
        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, platform.bundles, *bundles)
            self.assertEqual(
                expected_index(*bundles), platform.bundle_index()
            )

    def test_bundle_list(self):
        platform = platform_factory()
        bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(
                bundle_info=BundleInfo(version='1.1.0-1')
            ),
            bundle_resource_factory(
                bundle_info=BundleInfo(version='1.2.0-1')
            ),
        )
        with responses.RequestsMock() as rsps:
            add_json_bundle_index_response(rsps, platform.bundles, *bundles)
            self.assertEqual(
                sorted(expected_list(*bundles), key=lambda b: b['version']),
                sorted(platform.bundle_list(), key=lambda b: b['version'])
            )

    def test_bundle_metadata(self):
        platform = platform_factory()
        bundle = bundle_resource_factory()

        with responses.RequestsMock() as rsps:
            add_json_bundle_metadata_response(rsps, bundle)
            self.assertEqual(
                expected_metadata(bundle),
                platform.bundle_metadata(
                    bundle.python_tag, bundle.name, bundle.version
                )
            )

    def test_bundle_save(self):
        """Test saving a bundle to a local file."""
        platform = platform_factory()
        bundle = bundle_resource_factory()
        coll = bundle_collection_factory()
        tmpdir = mkdtemp()

        try:
            with responses.RequestsMock() as rsps:
                add_json_bundle_metadata_response(rsps, bundle)
                platform.bundle_save(
                    bundle.python_tag, bundle.name, bundle.version, tmpdir
                )
            from_file = coll.from_file(
                path.join(tmpdir, bundle.canonical_filename)
            )
            self.assertEqual(bundle, from_file)
        finally:
            rmtree(tmpdir)

    def test_bundle_save_exists(self):
        """Test saving a bundle to an existing local file."""
        platform = platform_factory()
        bundle = bundle_resource_factory()
        tmpdir = mkdtemp()
        exp_path = path.join(tmpdir, bundle.canonical_filename)

        try:
            with open(exp_path, 'w') as fp:
                fp.write('foo')

            with self.assertRaises(TargetFileExists):
                platform.bundle_save(
                    bundle.python_tag, bundle.name, bundle.version, tmpdir
                )

            with open(exp_path) as fp:
                self.assertEqual(fp.read(), 'foo')

        finally:
            rmtree(tmpdir)

    def test_bundle_save_exists_overwrite(self):
        """Test saving a bundle and overwriting a local file."""
        platform = platform_factory()
        bundle = bundle_resource_factory()
        coll = bundle_collection_factory()
        tmpdir = mkdtemp()
        exp_path = path.join(tmpdir, bundle.canonical_filename)

        try:
            with open(exp_path, 'w') as fp:
                fp.write('foo')

            with responses.RequestsMock() as rsps:
                add_json_bundle_metadata_response(rsps, bundle)
                platform.bundle_save(
                    bundle.python_tag, bundle.name, bundle.version, tmpdir,
                    overwrite=True
                )
            from_file = coll.from_file(exp_path)
            self.assertEqual(bundle, from_file)
        finally:
            rmtree(tmpdir)

    def test_bundle_upload(self):
        repo = repository_factory()
        overwrite = False
        with responses.RequestsMock() as rsps:
            bundle_info = BundleInfo()
            add_upload_bundle_response(
                rsps, bundle_resource_factory(bundle_info=bundle_info)
            )
            repo.upload_bundle(BUNDLE_PATH, overwrite=overwrite)
            assert_valid_bundle_upload(self, rsps, overwrite=overwrite)

    def test_bundle_upload_overwrite(self):
        repo = repository_factory()
        overwrite = True
        bundle_info = BundleInfo()
        with responses.RequestsMock() as rsps:
            add_upload_bundle_response(
                rsps, bundle_resource_factory(bundle_info=bundle_info)
            )
            repo.upload_bundle(BUNDLE_PATH, overwrite=overwrite)
            assert_valid_bundle_upload(self, rsps, overwrite=overwrite)
