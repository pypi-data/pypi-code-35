"""VSS Service Management plugin for VSS CLI (vss-cli)."""
import click
from vss_cli.cli import pass_context
from vss_cli import const
from vss_cli.config import Configuration
from vss_cli.helper import format_output


@click.group(
    'service',
    short_help='ITS Service catalog.'
)
@pass_context
def cli(ctx: Configuration):
    """Available ITS Service catalog."""
    ctx.load_config()


@cli.command(
    'ls',
    short_help='list available ITS Service catalog.'
)
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
def service_ls(
        ctx: Configuration, filter, page,
        sort, show_all, count
):
    """List services based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: valid,eq,false

            vss-cli service ls -f name,like,%VPN%

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli service ls -s label,desc

    """
    columns = ctx.columns or const.COLUMNS_VSS_SERVICE
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort
    # make request
    _requests = ctx.get_vss_services(
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
