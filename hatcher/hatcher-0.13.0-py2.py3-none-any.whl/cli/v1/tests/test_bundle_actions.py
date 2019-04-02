#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
"""Tests for bundle command-line options."""

from __future__ import absolute_import, print_function, unicode_literals

import json
from collections import namedtuple
from unittest import TestCase

from requests.exceptions import HTTPError

from hatcher.cli import main
from hatcher.core.model_registry import ModelRegistry
from hatcher.core.v1.repository import (
    Repository,
    SinglePlatformRepository as Platform
)
from hatcher.core.v1.tests.test_bundle import (
    BundleInfo,
    bundle_resource_factory,
    expected_index,
    expected_list,
    expected_index_metadata,
    expected_metadata,
)
from hatcher.errors import InvalidBundle, TargetFileExists
from hatcher.tests.common import (
    GenericNamespace,
    MainTestingMixin,
    Mock,
    patch
)
from hatcher.cli import utils


class HTTPErrFake(HTTPError):
    """ A simple mock for HTTP exceptions."""

    def __init__(self, status, msg, *args, **kwargs):
        """Set the ``response`` attribute appropriately."""
        super(HTTPErrFake, self).__init__(*args, **kwargs)
        self.response = GenericNamespace(
            status_code=status,
            headers={'Content-Type': 'application/json'},
            json=lambda *x, **y: {'error': msg}
        )


class TestBundleCommands(MainTestingMixin, TestCase):
    """ Test bundle CLI."""

    # Used in ``setup_mock_repo_class``
    PatchMocks = namedtuple('PatchMocks', ('repository', 'platform'))

    def setUp(self):
        """ Set common attributes for tests."""
        super(TestBundleCommands, self).setUp()
        self.initial_args = (
            '--api-version', '1',
            '--url', 'brood-dev.invalid',
            'bundles',
        )
        self.final_args = (self.organization, self.repository, self.platform)
        self.bundles = (
            bundle_resource_factory(),
            bundle_resource_factory(bundle_info=BundleInfo(name='newbundle')),
            bundle_resource_factory(bundle_info=BundleInfo(version='1.2.0-2')),
            bundle_resource_factory(bundle_info=BundleInfo(version='1.0.0-2')),
            bundle_resource_factory(bundle_info=BundleInfo(python_tag='cp27')),
        )

    def yield_args(self, *args, **kwargs):
        """ Return iterable initial args, specified args, and final args."""
        # Not including these as explicitly named keyword arguments b/c
        # Python 2 does not support named kwargs after *args.
        include_initial = kwargs.get('include_initial', True)
        include_final = kwargs.get('include_final', True)
        post_args = kwargs.get('post_args', ())
        if include_initial:
            for arg in self.initial_args:
                yield arg
        for arg in args:
            yield arg
        if include_final:
            for arg in self.final_args:
                yield arg
        for arg in post_args:
            yield arg

    def invoke(self, *args, **kwargs):
        """ Invoke the bundle CLI with the specified args."""
        return self.runner.invoke(
            main.hatcher,
            args=self.yield_args(*args, **kwargs)
        )

    def setup_mocked_repo_cls(self, mock_repo_cls):
        """Set the mock repo class up for later use."""
        mock_repo_cls.return_value = repo = Mock(spec=Repository)
        repo.organization_name = self.organization
        repo.name = self.repository
        repo.platform.return_value = platform = Mock(spec=Platform)
        return self.PatchMocks(repo, platform)

    class patches(object):
        """ Perform patches and return requested mocks as injected args.

        Patches the global Repository object in the ModelRegistry.
        Sets it to return a mocked ``Repository`` instance, which
        returns a mocked ``SinglePlatformRepository`` from its
        ``platform`` method.

        When instantiating the decorator, one or several of the
        attribute names on the NamedTuple returned by
        ``setup_mocked_repo_cls`` may be specified. For any specified
        attributes, their corresponding mocks will be injected, in
        the specified order, into the test function before any other
        arguments.
        """

        def __init__(self, *injections):
            """ Instantiate the fixture and determine what to inject."""
            self.injections = injections

        def __call__(self, meth):
            """ Return the method wrapper."""

            def wrapper(inner_self, *args, **kwargs):
                """ Patch resources, inject args, and call the method."""
                with patch.object(ModelRegistry, 'Repository') as MockRepo:
                    mocks = inner_self.setup_mocked_repo_cls(MockRepo)
                    injections = tuple(
                        getattr(mocks, i) for i in self.injections
                    )
                    return meth(
                        inner_self,
                        *(injections + args),
                        **kwargs
                    )

            return wrapper

    def test_help_no_error(self):
        """ Test we can call bundles --help."""
        result = self.invoke('--help')
        self.assertEqual(result.exit_code, 0)

    # ------------------------------------------------------------------
    # Collection Operations
    # ------------------------------------------------------------------

    @patches('platform')
    def test_list_bundles(self, mock_platform):
        """ Test the bundle list command."""
        mock_platform.bundle_list.return_value = expected_list(*self.bundles)
        res = self.invoke('list')

        self.assertEqual(res.exit_code, 0)
        mock_platform.bundle_list.assert_called_once_with()
        outlns = res.output.splitlines()

        exp_headers = ('Bundle Name', 'Bundle Version', 'Python Tag')
        self.assertTrue(all(i in outlns[0] for i in exp_headers))

        # After the headers is a line containing horizontal dividers.
        # Following is one bundle perline. Ensure we have the right
        # number of bundle lines.
        self.assertEqual(len(outlns[2:]), len(self.bundles))

        # Ensure that all of our bundles have their own line.
        for bun in self.bundles:
            self.assertEqual(
                1,
                len(tuple(
                    o for o in outlns if all(
                        i in o.split() for i in (
                            bun.name, bun.version, bun.python_tag
                        )
                    )
                ))
            )

        # Ensure our bundles are sorted (name, version, python_tag)
        prev = None
        for ln in outlns[2:]:
            bun = ln.split()  # (name, version, python_tag)
            if prev is not None:
                # Assert each item of our bundle tuple is literally less than
                # (string comparison) the item of the tuple before it.
                self.assertTrue(cur < prev for cur, prev in zip(bun, prev))
            prev = bun

    @patches('platform')
    def test_bundle_index(self, mock_platform):
        """ Test the bundle index command."""
        mock_platform.bundle_index.return_value = expected_index(*self.bundles)
        res = self.invoke('index')
        self.assertEqual(res.exit_code, 0)
        mock_platform.bundle_index.assert_called_once_with()
        for bundle in self.bundles:
            out = json.loads(res.output)
            ver, build = bundle.version.split('-')
            self.assertEqual(
                out[bundle.python_tag][bundle.name][ver][build],
                expected_index_metadata(bundle)
            )

    def _setup_bundle_repo_mock(self, mock_repo):
        """ Perform repetitive setup actions."""
        mock_repo.__str__ = lambda self: 'MockTestRepo'
        mock_repo.upload_bundle.return_value = GenericNamespace(
            upload_path='testupload.com'
        )

    @patches('repository')
    def test_bundle_upload(self, mock_repo):
        """ Test the bundle upload command."""
        # Ensure the click.echo() upload table can be printed
        self._setup_bundle_repo_mock(mock_repo)
        filepath = '/home/my_great_bundle-1.0.0-1.bundle'
        res = self.invoke(
            'upload',
            self.organization,
            self.repository,
            filepath,
            include_final=False,
        )
        self.assertEqual(res.exit_code, 0)
        mock_repo.upload_bundle.assert_called_once_with(
            filepath, overwrite=False
        )

        # (Kind of) check output table
        self.assertIn('Bundle upload', res.output)
        self.assertIn(filepath, res.output)
        self.assertIn('testupload.com', res.output)
        self.assertIn('MockTestRepo', res.output)

    @patches('repository')
    def test_bundle_upload_force(self, mock_repo):
        """ Test the bundle upload command."""
        # Ensure the click.echo() upload table can be printed
        self._setup_bundle_repo_mock(mock_repo)
        filepath = '/home/my_great_bundle-1.0.0-1.bundle'
        res = self.invoke(
            'upload',
            self.organization,
            self.repository,
            filepath,
            '--force',
            include_final=False,
        )
        self.assertEqual(res.exit_code, 0)
        mock_repo.upload_bundle.assert_called_once_with(
            filepath, overwrite=True
        )

        # (Kind of) check output table
        self.assertIn('Bundle upload', res.output)
        self.assertIn(filepath, res.output)
        self.assertIn('testupload.com', res.output)
        self.assertIn('MockTestRepo', res.output)

    def assert_bundle_upload_err_handled(self, mock_repo, err_inst, exp_msg,
                                         exp_rc=1, unexpected=False):
        """ Helper for asserting proper handling of bundle upload errors."""
        self._setup_bundle_repo_mock(mock_repo)
        filepath = '/home/my_great_bundle-1.0.0-1.bundle'
        mock_repo.upload_bundle.side_effect = err_inst
        res = self.invoke(
            'upload',
            self.organization,
            self.repository,
            filepath,
            include_final=False,
        )
        self.assertEqual(res.exit_code, exp_rc)
        mock_repo.upload_bundle.assert_called_once_with(
            filepath, overwrite=False
        )
        if unexpected:
            self.assertIn('Unexpected error', res.output)
        self.assertIn(exp_msg, res.output)

    @patches('repository')
    def test_bundle_upload_invalid_bundle(self, mock_repo):
        """ Test the bundle upload command."""
        msg = 'bundle invalid'
        self.assert_bundle_upload_err_handled(
            mock_repo, InvalidBundle(msg), msg, exp_rc=1
        )

    # Initially I wrote the tests below with the bundler inheriting
    # from the special HTTPErrorHandlingUploadCommand, but then decided
    # the default HTTP error handling was fine. Left these in to be sure
    # it's happening, but that is why the same exceptions are not
    # tested for the other remote commands.

    @patches('repository')
    def test_bundle_upload_401(self, mock_repo):
        """ Test the bundle upload raising a 403."""
        self.assert_bundle_upload_err_handled(
            mock_repo,
            HTTPErrFake(401, 'unauthorized'),
            'unauthorized',
            exp_rc=-1
        )

    @patches('repository')
    def test_bundle_upload_403(self, mock_repo):
        """ Test the bundle upload raising a 403."""
        self.assert_bundle_upload_err_handled(
            mock_repo,
            HTTPErrFake(403, 'forbidden'),
            'forbidden',
            exp_rc=-1,
        )

    @patches('repository')
    def test_bundle_upload_500(self, mock_repo):
        """ Test the bundle upload raising a 403."""
        self.assert_bundle_upload_err_handled(
            mock_repo,
            HTTPErrFake(403, 'Internal Server Error'),
            'Internal Server Error',
            exp_rc=-1,
        )

    # ------------------------------------------------------------------
    # Resource Operations
    # ------------------------------------------------------------------

    @patches('platform')
    def test_bundle_metadata(self, mock_platform):
        """ Test the bundle metadata command."""
        bundle = bundle_resource_factory(bundle_info=BundleInfo())
        mock_platform.bundle_metadata.return_value = expected_metadata(bundle)
        res = self.invoke(
            'metadata',
            post_args=(
                bundle.python_tag,
                bundle.name,
                bundle.version,
            )
        )
        self.assertEqual(res.exit_code, 0)
        mock_platform.bundle_metadata.assert_called_once_with(
            bundle.python_tag, bundle.name, bundle.version
        )
        out = json.loads(res.output)
        self.assertEqual(expected_metadata(bundle), out)

    @patches('platform')
    def test_bundle_download(self, mock_platform):
        """Test the bundle save command."""
        bundle = bundle_resource_factory(bundle_info=BundleInfo())
        mock_platform.bundle_save.return_value = 'mock_filepath'
        res = self.invoke(
            'download',
            post_args=(
                bundle.python_tag,
                bundle.name,
                bundle.version,
                'mock_directory',
            )
        )
        self.assertEqual(res.exit_code, 0)
        mock_platform.bundle_save.assert_called_once_with(
            bundle.python_tag, bundle.name, bundle.version, 'mock_directory',
            overwrite=False
        )
        self.assertIn('Bundle saved to mock_filepath', res.output)

    @patches('platform')
    def test_bundle_download_force(self, mock_platform):
        """Test the bundle save command."""
        bundle = bundle_resource_factory(bundle_info=BundleInfo())
        mock_platform.bundle_save.return_value = 'mock_filepath'
        res = self.invoke(
            'download',
            post_args=(
                bundle.python_tag,
                bundle.name,
                bundle.version,
                'mock_directory',
                '--force',
            )
        )
        self.assertEqual(res.exit_code, 0)
        mock_platform.bundle_save.assert_called_once_with(
            bundle.python_tag, bundle.name, bundle.version, 'mock_directory',
            overwrite=True
        )
        self.assertIn('Bundle saved to mock_filepath', res.output)

    @patches('platform')
    def test_bundle_download_exists_msg(self, mock_platform):
        """Test the downloading a bundle when a file exists."""
        bundle = bundle_resource_factory(bundle_info=BundleInfo())
        mock_platform.bundle_save.side_effect = TargetFileExists
        res = self.invoke(
            'download',
            post_args=(
                bundle.python_tag,
                bundle.name,
                bundle.version,
                'mock_directory',
            )
        )
        self.assertEqual(res.exit_code, 1)
        mock_platform.bundle_save.assert_called_once_with(
            bundle.python_tag, bundle.name, bundle.version, 'mock_directory',
            overwrite=False,
        )
        self.assertIn('bundle already exists', res.output)
