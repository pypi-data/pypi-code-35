#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
from __future__ import absolute_import, print_function

import click

from .main import hatcher
from .utils import pass_brood_client


@hatcher.group('organizations', api_versions=[0, 1])
def organizations():
    """Perform operations on organizations.
    """


@organizations.command(
    'create', help='Create a new organization.', api_versions=[0, 1])
@click.argument('name')
@click.argument('description')
@pass_brood_client
def create_organization(brood_client, name, description):
    brood_client.create_organization(name, description)


@organizations.command(
    'list', api_versions=[0, 1],
    help='List all of the organizations in a brood instance.')
@pass_brood_client
def list_organizations(brood_client):
    for organization in sorted(brood_client.list_organizations()):
        print(organization)
