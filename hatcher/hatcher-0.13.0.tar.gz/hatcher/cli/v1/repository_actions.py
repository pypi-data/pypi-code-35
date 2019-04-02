#  Copyright (c) 2013-2015, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE and may be redistributed only under the
#  conditions described in the aforementioned license.  The license is also
#  available online at https://opensource.org/licenses/BSD-3-Clause.
import json
import os
import sys

import click
from tabulate import tabulate

from hatcher.cli.repository_actions import runtimes, bundles
from hatcher.cli.utils import (
    HTTPErrorHandlingUploadCommand,
    pass_platform,
    pass_repository,
    print_dict,
    upload_context_table
)
from hatcher.core.utils import NameVersionPairSorter
from hatcher.errors import InvalidBundle, TargetFileExists


def print_success(msg):
    """Print a success message with click."""
    click.echo(click.style(msg, fg='green'))


def print_error(msg):
    """Print an error message with click."""
    click.echo(click.style(msg, fg='red'), err=True)


# ######################################################################
# Runtime Commands
# ######################################################################


@runtimes.command('list', api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@pass_repository
def list_runtimes_v1(repository, platform):
    """List all runtimes in a repository.
    """
    runtimes = sorted(
        repository.platform(platform).list_runtimes(),
        key=lambda runtime: NameVersionPairSorter(*runtime))
    headers = ['Runtime', 'Version']
    click.echo(tabulate(runtimes, headers=headers))


@runtimes.command('upload', help='Upload a single runtime to a repository.',
                  cls=HTTPErrorHandlingUploadCommand, api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('filename')
@click.option('--force', default=False, is_flag=True)
@click.option('--verify/--no-verify', default=False)
@click.pass_context
def upload_runtime_v1(ctx, organization, repository, filename, force, verify):
    repo = ctx.obj.organization(organization).repository(repository)
    context = upload_context_table(ctx, 'Runtime', filename, repo)
    click.echo(tabulate(context, tablefmt='plain'))
    repo.upload_runtime(filename, overwrite=force, verify=verify)


@runtimes.command('download', api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('implementation')
@click.argument('version')
@click.argument('destination', required=False)
@pass_repository
def download_runtime_v1(repository, platform, implementation, version,
                        destination=None):
    """Download a runtime archive.
    """

    if destination is None:
        destination = os.getcwd()

    length, iterator = repository.platform(platform).iter_download_runtime(
        implementation, version, destination)

    with click.progressbar(length=length) as bar:
        for chunk_size in iterator:
            bar.update(chunk_size)


@runtimes.command('metadata', help='Get the metadata for a single runtime.',
                  api_version=1)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('implementation')
@click.argument('version')
@pass_repository
def runtime_metadata_v1(repository, platform, implementation, version):
    metadata = repository.platform(platform).runtime_metadata(
        implementation, version)
    click.echo(json.dumps(metadata, sort_keys=True, indent=2))


# ######################################################################
# Bundle Commands
# ######################################################################


@bundles.command(
    'list',
    api_version=1,
    help='List all bundles for a given platform.'
)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@pass_platform
def list_bundles(platform):
    """Return a list of bundles for the given platform.

    Bundles are sorted in ascending alphanumerical order by name, then version,
    then python tag.
    """
    bundles = map(
        lambda b: (b['name'], b['version'], b['python_tag']),
        sorted(
            platform.bundle_list(),
            key=lambda b: '{name}:{version}:{python_tag}'.format(**b)
        )
    )
    headers = ('Bundle Name', 'Bundle Version', 'Python Tag')
    click.echo(tabulate(bundles, headers=headers))


@bundles.command(
    'index',
    api_version=1,
    help='Print the bundle index as a JSON object.'
)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@pass_platform
def bundle_index(platform):
    """Return a list of bundles for the given platform."""
    print_dict(platform.bundle_index())


@bundles.command(
    'metadata',
    api_version=1,
    help="Print a bundle's metadata as a JSON object."
)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('python_tag')
@click.argument('name')
@click.argument('version')
@pass_platform
def bundle_metadata(platform, python_tag, name, version):
    """Print metadata for the specified bundle."""
    print_dict(platform.bundle_metadata(python_tag, name, version))


@bundles.command(
    'download',
    api_version=1,
    help='Save bundle metadata to the specified directory.'
)
@click.argument('organization')
@click.argument('repository')
@click.argument('platform')
@click.argument('python_tag')
@click.argument('name')
@click.argument('version')
@click.argument('directory')
@click.option('--force', default=False, is_flag=True)
@pass_platform
def bundle_download(platform, python_tag, name, version, directory, force):
    """Save bundle metadata to a local file."""
    try:
        filepath = platform.bundle_save(
            python_tag, name, version, directory, overwrite=force
        )
    except TargetFileExists:
        print_error(
            'A bundle already exists in {} with name="{}" '
            'and version="{}". Add "--force" if you wish to '
            'overwrite it.'.format(directory, name, version)
        )
        sys.exit(1)
    click.echo('Bundle saved to {}'.format(filepath))


@bundles.command(
    'upload',
    api_version=1,
    help=(
        'Upload a bundle to a repo. The filename must be of the form '
        '<bundle_name>-<bundle_version>-<bundle_build>.bundle, e.g. '
        '"my_great_bundle-1.0.0-1.bundle".'
    ),
)
@click.argument('organization')
@click.argument('repository')
@click.argument('filename')
@click.option('--force', default=False, is_flag=True)
@pass_repository
@click.pass_context
def bundle_upload(ctx, repository, filename, force):
    """Upload a bundle to the server."""
    try:
        bundle = repository.upload_bundle(filename, overwrite=force)
        ctx.obj.url = bundle.upload_path
        context = upload_context_table(ctx, 'Bundle', filename, repository)
        click.echo(tabulate(context, tablefmt='plain'))
    except InvalidBundle as exc:
        print_error(str(exc))
        sys.exit(1)
    print_success('Successfully uploaded {}'.format(filename))
