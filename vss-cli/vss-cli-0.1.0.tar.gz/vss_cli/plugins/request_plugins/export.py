"""Vm Export Request Management plugin for VSS CLI (vss-cli)."""
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
    'export',
    short_help='Manage virtual machine export requests'
)
@pass_context
def request_mgmt_export(ctx: Configuration):
    """Manage virtual machine export requests."""
    pass


@request_mgmt_export.command(
    'ls',
    short_help='list vm export requests'
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
def request_mgmt_export_ls(ctx: Configuration, filter, page, sort,
                           show_all, count):
    """List requests based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: status,eq,Processed

            vss-cli request export ls -f status,eq,Processed

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli request export ls -s created_on,desc

    """
    columns = ctx.columns or const.COLUMNS_REQUEST_EXPORT_MIN
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort

    _requests = ctx.get_export_requests(
        show_all=show_all,
        per_page=count, **params)

    output = format_output(
        ctx,
        _requests,
        columns=columns
    )
    # page results
    if page:
        click.echo_via_pager(output)
    else:
        click.echo(output)


@request_mgmt_export.command(
    'get',
    short_help='Export request'
)
@click.argument(
    'rid', type=click.INT, required=True,
    autocompletion=autocompletion.export_requests
)
@pass_context
def request_mgmt_export_get(ctx: Configuration, rid):
    obj = ctx.get_export_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_EXPORT
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )
