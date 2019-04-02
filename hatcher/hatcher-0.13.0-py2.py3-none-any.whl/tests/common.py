#  Copyright (c) 2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
try:
    from unittest import mock
    from unittest.mock import Mock, patch
except ImportError:
    import mock  # noqa
    from mock import Mock, patch

from click.testing import CliRunner

from hatcher.cli import utils
from hatcher.core.brood_client import BroodClient as RealBroodClient
from hatcher.core.model_registry import ModelRegistry
from hatcher.core.v0.user import User as RealUser
from hatcher.core.v0.organization import Organization as RealOrganization
from hatcher.core.v0.repository import (
    Repository as RealRepository,
    SinglePlatformRepository,
)


patch_brood_client = patch.object(utils, 'BroodClient')
patch_organization = patch.object(ModelRegistry, 'Organization')
patch_repository = patch.object(ModelRegistry, 'Repository')
patch_team = patch.object(ModelRegistry, 'Team')
patch_user = patch.object(ModelRegistry, 'User')


if utils.IS_CLICK_7:
    CLIRUNNER_ERRCODE_ON_EXCEPTION = 1
else:
    CLIRUNNER_ERRCODE_ON_EXCEPTION = -1


class MainTestingMixin(object):

    def setUp(self):
        self.runner = CliRunner()
        self.organization = 'acme'
        self.repository = 'dev'
        self.team = 'dev-team'
        self.platform = 'rh5-64'
        self.user = 'user@acme.org'

    def tearDown(self):
        pass

    def _mock_brood_client_class(self, BroodClient):
        BroodClient.return_value = brood_client = Mock(
            spec=RealBroodClient)
        BroodClient.from_url.return_value = brood_client
        brood_client.organization.return_value = Mock(
            spec=RealOrganization)
        return brood_client

    def _mock_organization_class(self, Organization):
        Organization.return_value = organization = Mock(spec=RealOrganization)
        organization.repository.return_value = Mock(
            spec=RealRepository)
        return organization

    def _mock_repository_class(self, Repository):
        Repository.return_value = repo = Mock(spec=RealRepository)
        repo.organization_name = self.organization
        repo.name = self.repository
        repo.platform.return_value = platform_repo = Mock(
            spec=SinglePlatformRepository)
        return repo, platform_repo

    def _mock_user_class(self, User):
        User.return_value = user = Mock(spec=RealUser)
        user.email = self.user
        return user

    def assertOrganizationConstructedCorrectly(self, Organization):
        self.assertEqual(Organization.call_count, 1)
        self.assertEqual(
            Organization.call_args[0],
            (self.organization,),
        )
        self.assertIn('url_handler', Organization.call_args[1])

    def assertRepositoryConstructedCorrectly(self, Repository):
        self.assertEqual(Repository.call_count, 1)
        self.assertEqual(
            Repository.call_args[0],
            (self.organization, self.repository),
        )
        self.assertIn('url_handler', Repository.call_args[1])

    def assertTeamConstructedCorrectly(self, Team):
        self.assertEqual(Team.call_count, 1)
        self.assertEqual(
            Team.call_args[0],
            (self.organization, self.team),
        )
        self.assertIn('url_handler', Team.call_args[1])

    def assertUserConstructedCorrectly(self, User):
        self.assertEqual(User.call_count, 1)
        self.assertEqual(
            User.call_args[0],
            (self.organization, self.user),
        )
        self.assertIn('url_handler', User.call_args[1])

    def assert_called_once(self, mock_object):
        """Assert the passed mock object has been called exactly once.

        This method has been added to ``Mock`` as of Python 3.6, but
        it would fail silently in earlier Pythons due to the nature
        of attribute access on Mock objects.

        However, that was only true up to a certain version of ``mock``,
        which added an ``AttributeError`` for that particular attribute.
        This exposed a significant amount of code using
        ``assert_called_once()`` and having it succeed without actually
        asserting anything.

        Those calls have all been replaced with this method.
        """
        self.assertEqual(1, len(mock_object.mock_calls))


class GenericNamespace(object):
    """ A simple object for creating stubs/fakes/mocks/etc."""

    def __init__(self, **kwargs):
        """ Create a namespace with the specified key/value pairs."""
        for key, value in kwargs.items():
            setattr(self, key, value)
