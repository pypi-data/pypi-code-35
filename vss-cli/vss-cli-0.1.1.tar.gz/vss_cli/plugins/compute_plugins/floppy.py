import click
import logging
from vss_cli import const
from vss_cli.cli import pass_context
from vss_cli.config import Configuration
from vss_cli.helper import format_output
from vss_cli.plugins.compute import cli


_LOGGING = logging.getLogger(__name__)


@cli.group(
    'floppy',
    short_help='Manage floppy images.'
)
@pass_context
def compute_floppy(ctx: Configuration):
    """Available floppy images in both the VSS central store and your personal
    VSKEY-STOR space."""


@compute_floppy.group(
    'public',
    short_help='Browse public images'
)
@pass_context
def compute_floppy_public(ctx: Configuration):
    """Available Floppy images in the VSS central store"""


@compute_floppy_public.command(
    'ls',
    short_help='list floppy images'
)
@click.option('-f', '--filter', type=(str, str),
              default=(None, None),
              help='filter list by path or name')
@click.option('-s', '--sort', type=(str, str),
              default=(None, None),
              help='sort by name or path')
@click.option('-p', '--page', is_flag=True,
              help='page results in a less-like format')
@pass_context
def compute_floppy_public_ls(
        ctx: Configuration, filter, sort, page
):
    """List available Floppy images in the VSS central store.

    Filter by path or name path=<path> or name=<name>. For example:

        vss-cli compute floppy ls -f name like,pv% -s path asc
    """
    query = dict(expand=1)
    if filter:
        query['filter'] = '{},{}'.format(filter[0], filter[1])
    if sort:
        query['sort'] = '{},{}'.format(sort[0], sort[1])
    # get objects
    obj = ctx.get_floppies(**query)
    # format
    columns = ctx.columns or const.COLUMNS_IMAGE
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


@compute_floppy.group(
    'personal',
    short_help='Browse current user images'
)
@pass_context
def compute_floppy_personal(ctx):
    """Available Floppy images in your personal VSKEY-STOR space."""


@compute_floppy_personal.command(
    'ls',
    short_help='list personal Floppy images'
)
@click.option('-p', '--page', is_flag=True,
              help='page results in a less-like format')
@pass_context
def compute_floppy_personal_ls(
        ctx: Configuration, page
):
    """List available Floppy images stored in your personal VSKEY-STOR space.
    If the image you uploaded is not listing here, use the sync and try again.

        vss-cli compute floppy personal sync
        vss-cli compute floppy personal ls
    """
    obj = ctx.get_user_floppies()
    # format
    columns = ctx.columns or const.COLUMNS_IMAGE
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


@compute_floppy_personal.command(
    'sync',
    short_help='Sync personal Floppy images'
)
@pass_context
def compute_floppy_personal_sync(ctx: Configuration):
    """Synchronize ISO images stored in your personal VSKEY-STOR space. Once
    processed it should be listed with the ls command."""
    obj = ctx.sync_user_isos()
    columns = ctx.columns or const.COLUMNS_REQUEST_SUBMITTED
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )
