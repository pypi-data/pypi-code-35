#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from __future__ import absolute_import

from ..url_templates import URLS_V0


class Organization(object):
    """A representation of an organization in a Brood server.

       The object will use the V0 entrypoints.

    """

    def __init__(self, name, url_handler, model_registry):
        self.name = name
        self._url_handler = url_handler
        self._model_registry = model_registry
        self._urls = URLS_V0

    def __repr__(self):
        return '<{cls} organization_name={organization!r}>'.format(
            cls=type(self).__name__,
            organization=self.name,
        )

    def delete(self):
        """Delete this organization from Brood.

        """
        raise NotImplementedError('Not implemented in brood.')

    def metadata(self):
        """Get the metadata for this organization.

        """
        raise NotImplementedError('Not implemented in brood.')

    def list_repositories(self):
        """List all repositories in this organization.

        """
        path = self._urls.admin.organizations.repositories.format(
            organization_name=self.name,
        )
        data = self._url_handler.get_json(path)
        return data['repositories']

    def create_repository(self, name, description):
        """Create a new repository called ``name`` inside this organization.

        Parameters
        ----------
        name : str
            The name of the repository.
        description : str
            The description of the repository.

        Returns :class:`~hatcher.core.repository.Repository`

        """
        path = self._urls.admin.organizations.repositories.format(
            organization_name=self.name,
        )
        data = {
            "name": name,
            "description": description,
        }
        self._url_handler.post(path, data)
        return self.repository(name)

    def repository(self, name):
        """Get an existing repository.

        Parameters
        ----------
        name : str
            The name of the repository.

        Returns :class:`~hatcher.core.repository.Repository`

        """
        return self._model_registry.Repository(
            self.name, name, url_handler=self._url_handler,
            model_registry=self._model_registry)

    def list_users(self):
        """List all users in the organization.

        """
        raise NotImplementedError('Not implemented in brood.')

    def create_user(self, email, teams=None):
        """Create a new user

        Parameters
        ----------
        user_email : str
            The email address of the user.

        Returns :class:`~hatcher.core.user.User`

        """
        path = self._urls.admin.organizations.users.format(
            organization_name=self.name,
        )
        data = {
            'email': email,
        }
        if teams is not None:
            data['teams'] = [team.name for team in teams]
        self._url_handler.post(path, data=data)
        return self.user(email)

    def user(self, user_email):
        """Get the user with email ``user_email``.

        Parameters
        ----------
        user_email : str
            The email address of the user.

        Returns :class:`~hatcher.core.user.User`

        """
        return self._model_registry.User(
            self.name, user_email, url_handler=self._url_handler,
            model_registry=self._model_registry)
