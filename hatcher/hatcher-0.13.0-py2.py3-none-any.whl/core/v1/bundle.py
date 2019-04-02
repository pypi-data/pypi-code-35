#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
""" Provide interaction with server-side bundle resources."""

from __future__ import absolute_import, print_function, unicode_literals

import json
import re

from os import path

from hatcher.errors import InvalidBundle, TargetFileExists
from hatcher.core.utils import compute_sha256 as compute_hash
from hatcher.core.utils import python_tag


class BundleResourceController(object):
    """ A controller for bundle resource requests.

    Attributes
    ----------
    collection : BundleCollectionController
        The controller for this bundle's collection
    python_tag : str
        The python tag for the bundle resource
    name : str
        The name of the bundle resource
    version : str
        The full version (including build) of the bundle resource
    url_handler : BroodURLHandler
        A BroodURLHandler instance

    """

    BUNDLE_EXTENSION = 'bundle'
    BUNDLE_RE = re.compile(
        r"""
            (?P<name>[\.\w]+)
            -
            (?P<version>[^-]+)
            -
            (?P<build>\d+)
            \.{}$
        """.format(BUNDLE_EXTENSION),
        re.VERBOSE
    )

    def __init__(self, collection, python_tag, name, version):
        """ Instantiate a new BundleResourceController.

        Parameters
        ----------
        collection : BundleResourceCollection
            The bundle collection to which this bundle belongs
        python_tag : str
            The python tag (e.g. "cp36") of the bundle
        name : str
            The name of the bundle
        version : str
            The full version (including build number) of the bundle.
        filepath : str
            The path to a file used to create this controller, if
            applicable

        """
        self.collection = collection
        self.python_tag = python_tag
        self.name = name
        self.version = version
        self.url_handler = self.collection.url_handler

    def __eq__(self, other):
        """ Return whether two controllers are equivalent.

        Two controllers are equivalent if their respective bundle
        metadata is equivalent.
        """
        if self.python_tag != other.python_tag:
            return False
        if self.name != other.name:
            return False
        if self.version != other.version:
            return False
        self_plat = self.collection.platform
        other_plat = other.collection.platform
        if self_plat.organization_name != other_plat.organization_name:
            return False
        if self_plat.repository_name != other_plat.repository_name:
            return False
        if self_plat.name != other_plat.name:
            return False
        return True

    def __repr__(self):
        return (
            '<{0.__class__.__name__} '
            'organization={0.collection.platform.organization_name} '
            'repository={0.collection.platform.repository_name} '
            'platform={0.collection.platform.name} '
            'python_tag={0.python_tag} '
            'name={0.name} '
            'version={0.version}>'.format(self)
        )

    def __str__(self):
        return '{}/{}/{}/{}'.format(
            self.collection, self.python_tag, self.name, self.version
        )

    @property
    def canonical_filename(self):
        """ Return the expected filename for a bundle.

        The value is a `str`

        .. note::

          This is **NOT** a path and does **NOT** indicate that the
          bundle is associated with a real file on the filesystem.

        """
        return '{0.name}-{0.version}.{0.BUNDLE_EXTENSION}'.format(self)

    @property
    def lazy_dict(self):
        """ Lazily return a dict of local attributes.

         A dict representation of the bundle managed by the controller

        This property is explicitly lazy, in that it provides a
        representation of the resource without requiring any
        communication with the server.

        The lazy dict should contain enough information to build
        up a request to the Brood server if required.

        """
        return {
            'python_tag': self.python_tag,
            'name': self.name,
            'version': self.version,
        }

    @property
    def metadata_path(self):
        """ Return the metadata URL for the bundle.

        The value is a `str`

        """
        return self.collection.path('metadata', **vars(self))

    @property
    def upload_path(self):
        """ Return the path to which one may upload a bundle.

        The value is a `str`

        """
        return self.collection.path('upload')

    def metadata(self):
        """ Return the bundle's metadata from the brood server.

        Returns
        -------
        dict :
            The bundle metadata, which is currently of the form::

                {
                    'name': str,
                    'version': str,
                    'build': int,
                    'full_version': str,
                    'platform': str,
                    'data': {
                        **bundle_data
                    }
                }

        """
        return self.url_handler.get_json(self.metadata_path)

    def save(self, directory, overwrite=False):
        """ Save the bundle metadata to a file in the specified directory.

        This calls :meth:`metadata`, which is a remote operation.

        The bundle filename is automatically calculated based on the
        bundle name and version (see :meth:`canonical_filename` for
        details).

        Parameters
        ----------
        directory : str
            The path to a directory on the local filesystem
        overwrite : bool
            Whether an error should be raised if a file exists in the
            target location

        Returns
        -------
        str :
            The path to the saved bundle

        Raises
        ------
        TargetFileExists :
            if the target file exists

        """
        filepath = path.join(directory, self.canonical_filename)
        if path.exists(filepath) and not overwrite:
            raise TargetFileExists(filepath)
        with open(filepath, 'w') as bundlefile:
            json.dump(
                self.metadata()['data'],
                bundlefile,
                indent=2,
                sort_keys=True,
            )
        return filepath


class BundleResourceFileController(object):
    """ Controller for a bundle file associated with a bundle resource.

    Attributes
    ----------
    bundle : BundleResourceController
        The :class:`BundleResourceController` associated with this file
        controller
    filepath : str
        The path to the bundle file

    .. note::
        Any attributes not explicitly defined here are pulled from the
        ``bundle`` associated with the ``FileController``.
    """

    def __init__(self, bundle, filepath):
        """ Instantiate a BundleFileResourceController.

        Parameters
        ----------
        bundle : BundleResourceController
            A bundle controller to use as the basis for this bundle
            file controller. The bundle controller is used to determine
            not found in the bundle file, like ``name`` and ``version``
        filepath : str
            The path to the bundle file

        """
        self.bundle = bundle
        self.filepath = filepath

    def __eq__(self, other):
        """ Return whether two bundle file controllers are equal.

        The controllers are equal if their filepaths are equal AND
        they satisfy all conditions of equality for a
        :class:`BundleResourceController`.
        """
        if self.filepath != other.filepath:
            return False
        return self.bundle == other

    def __getattr__(self, attr):
        """ Return any attributes from the bundle if not defined here."""
        return getattr(self.bundle, attr)

    def __repr__(self):
        return (
            '<{0.__class__.__name__} '
            'bundle={0.bundle!r} '
            'filepath={0.filepath}>'.format(self)
        )

    def upload(self, overwrite=False):
        """ Upload the bundle file to the server.

        Parameters
        ----------
        overwrite : bool, optional
            whether the bundle should be overwritten if it already
            exists on the server

        """
        self.url_handler.upload(
            self.upload_path,
            self._upload_metadata(),
            self.filepath,
            overwrite=overwrite
        )

    def _upload_metadata(self):
        """ Return the expected metadata dict for the bundle file."""
        version, build = self.version.split('-')
        return {
            'sha256': compute_hash(self.filepath),
            'bundle_name': self.name,
            'bundle_version': version,
            'bundle_build': int(build),
        }


class BundleCollectionController(object):
    """ A controller for a collection of bundle resources.

    Attributes
    ----------
    platform : hatcher.core.v1.repository.SinglePlatformRepository
        a :class:`SinglePlatformRepository` instance, used to determine
        the organization name, repository name, and platform of
        bundle resources
    url_handler : hatcher.core.brood_url_handler.BroodURLHandler
        a :class:`BroodURLHandler` instance
    urls : Dict[str, hatcher.core.url_templates.UrlBuilder]
        a dict mapping hatcher method names (e.g. :meth:`index`) to
        :class:`UrlBuilder` instances, used in generating paths

    """

    def __init__(self, platform, url_template):
        """ Instantiate a BundleCollectionController.

        Parameters
        ----------
        platform : hatcher.core.v1.repository.SinglePlatformRepository
            a :class:`SinglePlatformRepository` instance, used to
            determine the organization name, repository name, and
            platform of bundle resources
        url_template: hatcher.core.url_templates.UrlBuilder
            a :class:`BroodURLHandler` instance to serve as the base
            for URL paths

        """
        self.platform = platform
        self.url_handler = self.platform._url_handler  # pylint: disable=W0212
        self.urls = {
            'index': url_template.indices.bundles,
            'metadata': url_template.metadata.artefacts.bundles,
            'upload': url_template.data.bundles.upload,
        }
        # The keys expected to be present in a metadata dictionary.
        self._metadata_signature = set(
            ('python_tag', 'name', 'full_version')
        )

    def __iter__(self):
        """ Iterate over BundleResourceControllers for this collection.

        .. warning::
            Because of the vagaries of the server, the only way to get
            information about a collection of bundles is to get the
            entire index. So, there's no efficient way to iterate over
            them. When such a capability is added, this method should
            be updated to use it. Until then, it's not very efficient.

        Yields
        ------
        BundleResourceController
            :class:`BundleResourceController` instances generated from
            bundles specified in the index

        """
        for bundle in self._bundles_from_index(self.index()):
            yield BundleResourceController(
                self,
                **self._bundle_list_item(bundle)
            )

    def __repr__(self):
        return (
            '<{0.__class__.__name__} '
            'organization={0.platform.organization_name} '
            'repository={0.platform.repository_name} '
            'platform={0.platform.name}>'.format(self)
        )

    def __str__(self):
        return '{}/bundles'.format(self.platform)

    @property
    def index_path(self):
        """ Return the path for retrieving the bundle index.

        The value is a `str`

        """
        return self.path('index')

    def from_file(self, filepath, runtime=None):
        """ Return a bundle instance as parsed from a bundlefile.

        Parameters
        ----------
        filepath : str
            The path to a bundlefile
        runtime : dict
            An optional dict describing the bundle's runtime. If not
            present, this will be parsed from the bundlefile.

        """
        if runtime is None:
            runtime = self._runtime_dict_from_bundle_file(filepath)
        name, version = self._name_and_version_from_filename(filepath)
        return BundleResourceFileController(
            BundleResourceController(
                self,
                python_tag(runtime['implementation'], runtime['version']),
                name,
                version,
            ),
            filepath
        )

    def get(self, python_tag, name, version):
        """ Return a BundleResourceController for the specified options.

        Parameters
        ----------
        python_tag : str
            The python tag (e.g. "cp36") of the bundle
        name : str
            The name of the bundle
        version : str
            The full version (including build number) of the bundle.

        Returns
        -------
        BundleResourceController :
            A controller for the requested bundle

        """
        return BundleResourceController(self, python_tag, name, version)

    def index(self):
        """ Return the bundle index for the parent platform.

        Returns
        -------
        dict :
            The bundle index, of the form::

                {
                    "python_tag": {
                        "name": {
                            "version": {
                                "build": {{metadata}},
                                ...
                            },
                            ...
                        },
                        ...
                    },
                    ...
                }

        """
        return self.url_handler.get_json(self.index_path)

    def list(self):
        """ Return a list of bundles info for the parent platform.

        .. warning::

            Because of the vagaries of the server, the only way to get
            information about a collection of bundles is to get the
            entire index. So, there's no efficient way to iterate over
            them. When such a capability is added, this method should
            be updated to use it. Until then, it's not very efficient.


        Returns
        -------
        list :
            A list of bundle metadata dictionaries from the index,
            filtered by field mask

        """
        return list(
            self._bundle_list_item(b)
            for b in self._bundles_from_index(self.index())
        )

    def path(self, operation, **kwargs):
        """ Return the Brood URL for the specified bundle.

        Parameters
        ----------
        operation: str
            One of the operations specified in ``self.urls``
        ``**kwargs`` :
            Extra keyword arguments to pass to the format operator for
            the specified URL base

        Returns
        -------
        str :
            The bundle download URL

        """
        return self.urls[operation].format(
            organization_name=self.platform.organization_name,
            repository_name=self.platform.repository_name,
            platform=self.platform.name,
            **kwargs
        )

    def _bundles_from_index(self, index):
        """ Yield bundle metadata dicts from the index.

        Metadata dictionaries contain several key/value pairs whose
        values are simple strings, along with a "data" key whose value
        is a large dictionary corresponding to the bundle specification.

        The index is a dictionary whose top-level keys are python tags,
        second level keys are bundle names, third level keys are bundle
        versions, and last level keys are bundle build numbers. The
        value at the end is a metadata dictionary.

        To get bundles from the index, we don't actually need anything
        from any level of the dictionary outside of the final metadata
        dictionary, which contains all the information included above.
        So, we traverse the tree until we find a node whose keys contain
        all of the expected metadata keys defined in
        ``self._metadata_signature`` (other keys may also be present),
        yield that node, and continue.
        """
        if not self._metadata_signature.difference(set(index)):
            yield index
        else:
            for val in index.values():
                for bundle in self._bundles_from_index(val):
                    yield bundle

    @staticmethod
    def _bundle_list_item(metadata):
        """ Return bits of metadata required for a bundle list item."""
        try:
            return {
                'python_tag': metadata['python_tag'],
                'name': metadata['name'],
                'version': metadata['full_version'],
            }
        except KeyError as exc:
            raise InvalidBundle(
                'Could not parse metdata ({}): {}'.format(exc, metadata)
            )

    @staticmethod
    def _name_and_version_from_filename(name_or_path):
        """ Return (name, version) from the specified file."""
        match = BundleResourceController.BUNDLE_RE.match(
            path.basename(name_or_path)
        )
        if match is None:
            raise InvalidBundle(
                'Bundle filename must be of the form '
                '"<bundle_name>-<version>-<build>.bundle"'
            )
        groups = match.groups()
        return groups[0], '-'.join(groups[1:])

    @staticmethod
    def _runtime_dict_from_bundle_file(filepath):
        """ Return a runtime dict parsed from a bundlefile."""
        try:
            with open(filepath) as bundle_file:
                try:
                    return json.load(bundle_file)['runtime']
                except KeyError:
                    raise InvalidBundle('Bundle does not have "runtime" key')
        except (IOError, OSError) as exc:
            raise InvalidBundle(exc)


class BundleControllerFactory(object):
    """ Create bundle controllers.

    Attributes
    ----------
    repository : brood.core.v1.repository.Repository
        The repository for which the controllers will be created
    url_template : brood.core.url_templates.UrlBuilder
        An instance of :class:`UrlBuilder` to serve as the base for
        generated URLs

    """

    def __init__(self, repository, url_template):
        """ Instantiate a BundleControllerFactory.

        Parameters
        ----------
        repository : brood.core.v1.repository.Repository
            The repository for which the controllers will be created
        url_template : brood.core.url_templates.UrlBuilder
            An instance of :class:`UrlBuilder` to serve as the base for
            generated URLs

        """
        self.repository = repository
        self.url_template = url_template

    def from_file(self, filepath):
        """ Create BundleResourceFileController from a bundle file.

        Parameters
        ----------
        filepath : str
            The path to the bundle file
        name : str
            The name of the bundle
        version : str
            The full version of the bundle, including build

        Returns
        -------
        BundleResourceFileController :
            A file controller for the specified bundle file and info

        """
        runtime = BundleCollectionController._runtime_dict_from_bundle_file(
            filepath
        )
        coll = BundleCollectionController(
            self.repository.platform(runtime['platform']),
            self.url_template,
        )
        return coll.from_file(filepath, runtime=runtime)

    def from_runtime_dict(self, runtime, name, version):
        """ Create a BundleResourceController from a runtime dict.

        Parameters
        ----------
        runtime : dict
            A dict of python runtime data. This must contain, minimally,
            keys "platform", "implementation", and "version"
        name : str
            The name of the bundle
        version : str
            The full version of the bundle, including build

        Returns
        -------
        BundleResourceController :
            A bundle controller for the specified runtime and bundle
            data

        """
        plat = self.repository.platform(runtime['platform'])
        coll = BundleCollectionController(plat, self.url_template)
        py_tag = python_tag(runtime['implementation'], runtime['version'])
        return coll.get(py_tag, name, version)
