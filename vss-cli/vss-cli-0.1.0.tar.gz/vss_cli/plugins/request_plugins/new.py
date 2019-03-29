"""New VM Request Management plugin for VSS CLI (vss-cli)."""
import click
import logging

from vss_cli import const
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output
from vss_cli.plugins.request import cli


_LOGGING = logging.getLogger(__name__)


@cli.group(
    'new',
    short_help='Manage new virtual machine deployment requests'
)
@pass_context
def request_mgmt_new(ctx: Configuration):
    """Manage new virtual machine deployment requests"""
    pass


@request_mgmt_new.command(
    'ls', short_help='list vm new requests'
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
def request_mgmt_new_ls(
        ctx: Configuration, filter, page, sort,
        show_all, count
):
    """List requests based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: status,eq,Processed

            vss-cli request new ls -f status,eq,Processed

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli request new ls -s created_on,desc

    """
    columns = ctx.columns or const.COLUMNS_REQUEST_NEW_MIN
    _LOGGING.debug(f'Columns {columns}')
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort

    _requests = ctx.get_new_requests(
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


@request_mgmt_new.command(
    'get',
    short_help='New vm request'
)
@click.argument('rid', type=click.INT, required=True)
@pass_context
def request_mgmt_new_get(
    ctx: Configuration,
    rid
):
    obj = ctx.get_new_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_NEW
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )


@request_mgmt_new.command(
    'retry',
    short_help='Retry vm new request'
)
@click.argument('rid', type=click.INT, required=True)
@pass_context
def request_mgmt_new_retry(ctx: Configuration, rid):
    """Retries given virtual machine new request with status
    'Error Processed'.
    """
    obj = ctx.retry_new_request(rid)
    columns = ctx.columns or const.COLUMNS_REQUEST_SUBMITTED
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )
