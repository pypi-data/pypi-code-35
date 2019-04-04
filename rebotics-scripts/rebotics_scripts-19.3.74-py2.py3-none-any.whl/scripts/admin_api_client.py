from multiprocessing.pool import Pool

import click
from prettytable import PrettyTable

from sdk.providers import AdminProvider, RetailerProvider


@click.group()
@click.option('-h', '--host')
# @click.option('-u', '--user', prompt=True, )
# @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.pass_context
def api(ctx, host):
    """
    This action will login you into retailer that you provide.
    """
    ctx.ensure_object(dict)
    provider = AdminProvider(host=host, retries=1)
    # try:
    #     provider.api_login(user, password)
    #     click.echo("Successfully logged in for retailer", err=True)
    # except ProviderHTTPClientException:
    #     raise ProviderHTTPClientException("Failed To login")
    ctx.obj['provider'] = provider


def get_retailer_version(retailer_dict):
    retailer_provider = RetailerProvider(host=retailer_dict['host'], retries=1)
    try:
        version = retailer_provider.version()
    except Exception:
        version = 'not working'

    d = [
        retailer_dict['codename'],
        retailer_dict['title'],
        version,
        retailer_dict['host']
    ]
    return d


@api.command()
@click.pass_context
def retailer_versions(ctx):
    provider = ctx.obj['provider']
    retailers = provider.get_retailer_list()

    pool = Pool(len(retailers))
    results = pool.map(get_retailer_version, retailers)

    table = PrettyTable()
    table.field_names = ['codename', 'title', 'version', 'host']
    for result in results:
        table.add_row(result)
    click.echo(table)
