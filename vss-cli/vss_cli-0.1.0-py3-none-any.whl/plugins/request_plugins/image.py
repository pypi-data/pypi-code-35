"""Image Sync Request Management plugin for VSS CLI (vss-cli)."""
import click
import logging

from vss_cli import const
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output
from vss_cli.plugins.request import cli

import vss_cli.autocompletion as autocompletion


_LOGGING = logging.getLogger(__name__)


@cli.group(
    'image',
    short_help='Manage user-image synchronization requests'
)
@pass_context
def image_sync(ctx: Configuration):
    """Synchronizing your personal store files with the VSS API produces a
    image-sync request"""


@image_sync.command(
    'ls',
    short_help='list image-sync requests'
)
@click.option('-f', '--filter', type=click.STRING,
              help='apply filter')
@click.option('-s', '--sort', type=click.STRING,
              help='apply sorting ')
@click.option('-a', '--show-all', is_flag=True,
              help='show all results')
@click.option('-c', '--count', type=click.INT,
              help='size of results')
@click.option('-p', '--page', is_flag=True,
              help='page results in a less-like format')
@pass_context
def image_sync_ls(
        ctx: Configuration, filter, page,
        sort, show_all, count):
    """List requests based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: status,eq,Processed

            vss-cli request image-sync ls -f status,eq,Processed

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli request image-sync ls -s created_on,desc

    """
    columns = ctx.columns or const.COLUMNS_REQUEST_IMAGE_SYNC_MIN
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort
    # make request
    _requests = ctx.get_image_sync_requests(
        show_all=show_all,
        per_page=count, **params)
    # format output
    output = format_output(
        ctx,
        _requests,
        columns=columns,
    )
    # page results
    if page:
        click.echo_via_pager(output)
    else:
        click.echo(output)


@image_sync.command(
    'get',
    help='Image sync request'
)
@click.argument(
    'rid', type=click.INT, required=True,
    autocompletion=autocompletion.image_sync_requests
)
@pass_context
def image_sync_get(ctx, rid):
    obj = ctx.get_image_sync_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_IMAGE_SYNC
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )
