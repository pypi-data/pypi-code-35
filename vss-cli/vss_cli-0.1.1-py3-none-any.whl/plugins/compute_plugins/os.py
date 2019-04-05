import click
import logging
from vss_cli import const
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output
from vss_cli.plugins.compute import cli


_LOGGING = logging.getLogger(__name__)


@cli.group(
    'os',
    short_help='Supported OS.'
)
@pass_context
def compute_os(ctx):
    """Supported operating systems by our infrastructure.
    This resource is useful when deploying a new or
    reconfiguring an existing virtual machine."""


@compute_os.command('ls', short_help='list operating systems')
@click.option('-f', '--filter', type=click.STRING,
              help='apply filter')
@click.option('-s', '--sort', type=click.STRING,
              help='apply sorting ')
@click.option('-a', '--show-all', is_flag=True,
              help='show all results')
@click.option('-c', '--count', type=int,
              help='size of results')
@click.option('-p', '--page', is_flag=True,
              help='page results in a less-like format')
@pass_context
def compute_os_ls(
        ctx: Configuration, filter,
        page, sort, show_all, count):
    """List requests based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: status,eq,Processed

            vss-cli compute os ls -f guestFullName,like,CentOS%

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli compute os ls -s guestId,asc

    """
    query = dict()
    if filter:
        query['filter'] = filter
    if sort:
        query['sort'] = sort

    obj = ctx.get_os(show_all=show_all,
                     per_page=count,
                     **query)
    # format
    columns = ctx.columns or const.COLUMNS_OS
    output = format_output(
        ctx,
        obj,
        columns=columns,
    )
    # page results
    if page:
        click.echo_via_pager(output)
    else:
        click.echo(output)
