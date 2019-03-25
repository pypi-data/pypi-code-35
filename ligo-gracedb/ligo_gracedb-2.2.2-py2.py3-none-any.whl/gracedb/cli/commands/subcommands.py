import argparse
import os
import six
import sys
import textwrap

from .base import RegisteredSubCommandBase
from ..parsers import (
    object_id_parser, superevent_id_parser, graceid_parser, comment_parser,
    tag_parser, label_parser,
)


class ConfirmAsGwCommand(RegisteredSubCommandBase):
    name = "confirm_as_gw"
    description = "Confirm a superevent as a GW"
    long_description = textwrap.dedent("""\
        Confirm a superevent as a gravitational wave. Specific permissions are
        required to perform this action on non-Test superevents.
    """).rstrip()
    parent_parsers = (superevent_id_parser,)

    def run(self, client, args):
        return client.confirm_superevent_as_gw(args.superevent_id)


class CredentialsCommand(RegisteredSubCommandBase):
    name = "credentials"
    description = "Display your credentials"
    long_description = textwrap.dedent("""\
        Display credentials that the client will use to make API requests.
        Useful for checking that your credentials are being found as expected.
    """).rstrip()

    def run(self, client, args):
        return client.show_credentials(print_output=False)


class ExposeCommand(RegisteredSubCommandBase):
    name = "expose"
    description = "Expose a superevent to non-internal users"
    long_description = textwrap.dedent("""\
        Expose a superevent to LV-EM and public users. Special permissions
        are required to perform this action.
    """).rstrip()

    def add_custom_arguments(self, parser):
        parser.add_argument('superevent_id', type=str,
            help="ID of the superevent to expose")
        return parser

    def run(self, client, args):
        return client.modify_permissions(args.superevent_id, 'expose')


class HideCommand(RegisteredSubCommandBase):
    name = "hide"
    description = \
        "Make an exposed superevent accessible to internal users only"
    long_description = textwrap.dedent("""\
        Make a superevent accessible to internal users only. Specific
        permissions are required to perform this action.
    """).rstrip()

    def add_custom_arguments(self, parser):
        parser.add_argument('superevent_id', type=str,
            help="ID of the superevent to hide")
        return parser

    def run(self, client, args):
        return client.modify_permissions(args.superevent_id, 'hide')


class PingCommand(RegisteredSubCommandBase):
    name = "ping"
    description = \
        "Make a basic request to check your connection to the server"

    def run(self, client, args):
        response = client.ping()
        output = 'Response from {server}: {status}'.format(
            server=client._service_url, status=response.status)
        if (response.status == 200):
            output += ' OK'
        return output


class ShowCommand(RegisteredSubCommandBase):
    """
    These commands all just print basic information obtained from the API root
    and attached to the client instance as a property. Each dict in 'options'
    corresponds to a command.
    """
    name = "show"
    description = textwrap.dedent("""\
        Show available EM groups, LVC analysis groups, pipelines, searches,
        labels, signoff types, signoff statuses, superevent categories,
        or VOEvent types
    """).rstrip()

    # Mapping from argument value to client property
    options = {
        'emgroups': 'em_groups',
        'groups': 'groups',
        'instruments': 'instruments',
        'labels': 'allowed_labels',
        'pipelines': 'pipelines',
        'searches': 'searches',
        'signoff_statuses': 'signoff_statuses',
        'signoff_types': 'signoff_types',
        'superevent_categories': 'superevent_categories',
        'voevent_types': 'voevent_types',
    }

    def add_custom_arguments(self, parser):
        parser.add_argument("items", type=str,
            choices=sorted(list(self.options)),
            help="List of objects to display")
        return parser

    def run(self, client, args):
        # Get list of objects from server, sort, and print
        data = getattr(client, self.options.get(args.items))
        if isinstance(data, dict):
            data = ['{k} ({v})'.format(k=k, v=v) for k,v in
                six.iteritems(data)]
        return ", ".join(sorted(data))
