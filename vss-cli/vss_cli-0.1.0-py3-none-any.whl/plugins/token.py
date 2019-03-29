"""Token Management plugin for VSS CLI (vss-cli)."""
import click
from vss_cli.cli import pass_context
from vss_cli import const
from vss_cli.config import Configuration
from vss_cli.helper import format_output


@click.group(
    'token',
    short_help='Manage access tokens'
)
@pass_context
def cli(ctx: Configuration):
    """Manage access tokens."""
    ctx.load_config()


@cli.command(
    'ls',
    short_help='list user tokens'
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
def token_ls(
        ctx: Configuration, filter, page,
        sort, show_all, count
):
    """List tokens based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: valid,eq,false

            vss-cli token ls -f valid,eq,false

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli token ls -s created_on,desc

    """
    columns = ctx.columns or const.COLUMNS_TK
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort
    # make request
    _requests = ctx.get_user_tokens(
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


@cli.command(
    'get',
    help='Token'
)
@click.argument('tid', type=int, required=True)
@pass_context
def token_get(ctx: Configuration, tid):
    obj = ctx.get_user_token(tid)
    columns = ctx.columns or const.COLUMNS_TK
    if not ctx.columns:
        columns.extend(
            [('VALID', 'status.valid'),
             ('VALUE', 'value')]
        )
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )


@cli.command(
    'rm',
    help='Delete user token.'
)
@click.argument('tid', type=int, required=True, nargs=-1)
@click.option('-s', '--summary', is_flag=True,
              help='Print request summary')
@pass_context
def token_rm(ctx: Configuration, tid, summary):
    result = []
    with click.progressbar(tid) as ids:
        for i in ids:
            result.append(ctx.delete_user_token(i))
    if summary:
        for res in result:
            click.echo(
                format_output(
                    ctx,
                    [res],
                    columns=[('STATUS', 'status')],
                    single=True
                )
            )
