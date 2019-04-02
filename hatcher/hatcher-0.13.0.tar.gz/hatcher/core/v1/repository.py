#  Copyright (c) 2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
""" V1 Repository and Platform (SinglePlatformRepository)."""

from hatcher.core.url_templates import URLS_V1
from hatcher.core.v0.repository import (
    Repository as RepositoryV0,
    SinglePlatformRepository as SinglePlatformRepositoryV0,
)
from hatcher.core.utils import RuntimeMetadataV1, upload_verify

from .bundle import BundleCollectionController, BundleControllerFactory


# Extend SinglePlatformRepositoryV0 as we just override runtime
# handling.
class SinglePlatformRepository(SinglePlatformRepositoryV0):

    def __init__(self, repository, platform, url_handler, model_registry):
        super(SinglePlatformRepository, self).__init__(
            repository, platform, url_handler, model_registry
        )
        self._urls = URLS_V1  # Make sure that we use the V1 entry points
        self.bundles = BundleCollectionController(self, self._urls)

    # ------------------------------------------------------------------
    # Runtimes
    # ------------------------------------------------------------------

    def list_runtimes(self):
        """List all runtimes in a repository.

        """
        index = self.runtime_index()
        runtimes = [
            (implementation, version)
            for implementation, idict in index.items()
            for version in idict.keys()
        ]
        return runtimes

    def runtime_index(self):
        """Get the index of all the runtimes in the current repository

        """
        # FIXME: This works by downloading and parsing the index.  We
        # probably want to expose a list_runtimes endpoint in brood.
        index_path = self._urls.indices.runtimes.format(
            organization_name=self.organization_name,
            repository_name=self.repository_name,
            platform=self.name,
        )
        return self._url_handler.get_json(index_path)

    def runtime_metadata(self, implementation, version):
        """Fetch the metadata for a runtime.

        """
        path = self._runtime_url(
            self._urls.metadata.artefacts.runtimes, implementation, version)
        return self._url_handler.get_json(path)

    def _download_runtime(self, implementation, version, destination,
                          download_file, expected_sha256):
        if expected_sha256 is None:
            metadata = self.runtime_metadata(implementation, version)
            expected_sha256 = metadata['sha256']

        path = self._runtime_url(
            self._urls.data.runtimes.download, implementation, version)
        return download_file(path, destination, expected_sha256)

    def download_runtime(self, implementation, version, destination,
                         expected_sha256=None):
        """Download a runtime and save it in the given directory.

        """
        self._download_runtime(
            implementation, version, destination,
            self._url_handler.download_file, expected_sha256=expected_sha256)

    def iter_download_runtime(self, implementation, version, destination,
                              expected_sha256=None):
        """Download a runtime and save it in the given directory.

        This method returns a tuple of (content_length, iterator).  The
        ``content_length`` is the total size of the download.  The
        ``iterator`` yield the size of each chunk as it is downloaded.

        """
        return self._download_runtime(
            implementation, version, destination,
            self._url_handler.iter_download, expected_sha256=expected_sha256)

    def _runtime_url(self, base, implementation, version):
        return base.format(
            organization_name=self.organization_name,
            repository_name=self.repository_name,
            platform=self.name,
            implementation=implementation,
            version=version,
        )

    # ------------------------------------------------------------------
    # Bundles
    # ------------------------------------------------------------------

    def bundle_index(self):
        """ Return the index of all bundles for this platform.

        Returns
        -------
        result : dict
            Same output as :meth:`~bundle.BundleCollectionController.index`

        """
        return self.bundles.index()

    def bundle_list(self):
        """ Return a list of bundles for this platform.

        .. note::
            This calls :meth:`~bundle.BundleCollectionController.index`
            behind the scenes, so if you need any additional metadata
            other than the default fields provided here, you may as
            well call that and then parse the index, rather than
            propagating extra server calls based on the return from
            this method.

        Returns
        -------
        result : list
            A list of dictionaries same output as
            :meth:`~bundle.BundleCollectionController.list`

        """
        return self.bundles.list()

    def bundle_metadata(self, python_tag, name, version):
        """ Return the metadata for the specified bundle.

        Parameters
        ----------
        python_tag : str
            The Python runtime compatibility of the egg, as defined in
            the ``Python Tag`` section of PEP425.
        name : str
            The name of the egg.
        version : str
            The full version specification of the egg.

        Returns
        -------
        dict :
            The bundle metadata
        """
        return self.bundles.get(python_tag, name, version).metadata()

    def bundle_save(self, python_tag, name, version, directory,
                    overwrite=False):
        """ Save bundle metadata to a file.

        Parameters
        ----------
        python_tag : str
            The Python runtime compatibility of the egg, as defined in
            the ``Python Tag`` section of PEP425.
        name : str
            The name of the egg.
        version : str
            The full version specification of the egg.

        Returns
        -------
        dict :
            The bundle metadata
        """
        return self.bundles.get(python_tag, name, version).save(
            directory, overwrite=overwrite
        )


# Extend RepositoryV0 as we just override runtime handling.
class Repository(RepositoryV0):

    def __init__(self, organization_name, name, url_handler, model_registry):
        super(Repository, self).__init__(
            organization_name, name, url_handler, model_registry)
        self._urls = URLS_V1  # Make sure that we use the V1 entry points

    def upload_runtime(self, filename, overwrite=False, verify=False):
        """Upload a runtime.

        """
        metadata = RuntimeMetadataV1.from_file(filename)
        metadata_dict = {'sha256': metadata.sha256}
        path = self._urls.data.runtimes.upload.format(
            organization_name=self.organization_name,
            repository_name=self.name,
            platform=metadata.platform,
        )

        def do_upload():
            self._url_handler.upload(
                path, metadata_dict, filename, overwrite=overwrite)

        def get_remote_metadata(local_metadata):
            platform_repo = self.platform(local_metadata.platform)
            return platform_repo.runtime_metadata(
                local_metadata.implementation, local_metadata.version)

        upload_verify(
            filename, metadata, get_remote_metadata, do_upload,
            verify=verify, overwrite=overwrite)

    def upload_bundle(self, filepath, overwrite=False):
        """ Upload a bundle to the server.

        Parameters
        ----------
        filepath : str
            The path to the bundle file to upload
        overwrite : bool
            If provided, the upload will overwrite an existing bundle
            matching the python tag (parsed from the bundle file),
            name, and version provided
        """
        bundle = BundleControllerFactory(self, self._urls).from_file(filepath)
        bundle.upload(overwrite=overwrite)
        return bundle
