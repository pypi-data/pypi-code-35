#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from __future__ import absolute_import

from ..url_templates import URLS_V0


class User(object):

    def __init__(self, organization_name, email, url_handler, model_registry):
        self.organization_name = organization_name
        self.email = email
        self._url_handler = url_handler
        self._model_registry = model_registry
        self._urls = URLS_V0

    def __repr__(self):
        return '<{cls} organization={organization!r}, email={email!r}>'.format(
            cls=type(self).__name__,
            organization=self.organization_name,
            email=self.email,
        )

    def delete(self):
        """Delete this user from the brood server.

        """
        path = self._urls.admin.users.metadata.format(
            organization_name=self.organization_name,
            email=self.email,
        )
        self._url_handler.delete(path)

    def metadata(self):
        """Get the user's metadata.

        """
        path = self._urls.admin.users.metadata.format(
            organization_name=self.organization_name,
            email=self.email,
        )
        return self._url_handler.get_json(path)
