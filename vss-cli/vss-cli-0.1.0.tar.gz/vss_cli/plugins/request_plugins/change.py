"""Vm Change Request Management plugin for VSS CLI (vss-cli)."""
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
    'change',
    short_help='Manage virtual machine change requests'
)
@pass_context
def request_mgmt_change(ctx: Configuration):
    """ Updating any virtual machine attribute
    will produce a virtual machine change request."""
    pass


@request_mgmt_change.command(
    'ls',
    short_help='list vm change requests'
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
def request_mgmt_change_ls(
        ctx: Configuration, filter, page, sort,
        show_all, count
):
    """List requests based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: status,eq,Processed

            vss-cli request change ls -f status,eq,Processed

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli request change ls -s created_on,desc

    """
    columns = ctx.columns or const.COLUMNS_REQUEST_CHANGE_MIN
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort

    _requests = ctx.get_change_requests(
        show_all=show_all,
        per_page=count, **params)

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


@request_mgmt_change.command(
    'get',
    short_help='Change request'
)
@click.argument(
    'rid', type=click.INT,
    required=True,
    autocompletion=autocompletion.change_requests
)
@pass_context
def request_mgmt_change_get(ctx: Configuration, rid):
    obj = ctx.get_change_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_CHANGE
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )


@request_mgmt_change.command(
    'retry',
    short_help='Retry vm change request'
)
@click.argument(
    'rid', type=click.INT,
    required=True,
    autocompletion=autocompletion.change_requests
)
@pass_context
def request_mgmt_change_retry(ctx: Configuration, rid):
    """Retries given virtual machine change request with status
    'Error Processed'.
    """
    obj = ctx.retry_change_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_SUBMITTED
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )
