import datetime
import json
import os
from multiprocessing.pool import Pool

import click
import humanize
from prettytable import PrettyTable

from sdk.providers import AdminProvider, RetailerProvider
from sdk.utils import mkdir_p


@click.group()
@click.option('-h', '--host')
@click.version_option()
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
        response = retailer_provider.version()
        version = response['version']
        uptime = humanize.naturaldelta(datetime.timedelta(seconds=int(response['uptime'])))
    except Exception:
        version = 'not working'
        uptime = '---'

    d = [
        retailer_dict['codename'],
        retailer_dict['title'],
        version,
        uptime,
        retailer_dict['host'],
    ]
    return d


@api.command()
@click.pass_context
def generate_retailer_configurations(ctx):
    provider = ctx.obj['provider']
    retailers = provider.get_retailer_list()

    pool = Pool(len(retailers))
    results = pool.map(get_retailer_version, retailers)

    retailers_conf_path = os.path.expanduser('~/.rebotics-scripts/retailers.json')
    try:
        with open(retailers_conf_path, 'r') as fin:
            retailers_conf = json.load(fin)
    except FileNotFoundError:
        mkdir_p(os.path.expanduser('~/.rebotics-scripts'))
        with open(retailers_conf_path, 'w') as fout:
            json.dump({}, fout)
            retailers_conf = {}

    current_retailers = retailers_conf.get(provider.domain, {})

    active_retailers = {}
    for codename, title, version, uptime, host in results:
        if version != 'not working':
            active_retailers[codename] = {
                'title': title,
                'codename': codename,
                'version': version,
                'host': host,
                'is_active': True,
            }

    current_retailers_hosts = current_retailers.keys()
    active_retailers_hosts = active_retailers.keys()

    retailers_to_override = active_retailers_hosts & current_retailers_hosts
    retailers_to_add = active_retailers_hosts - current_retailers_hosts
    retailers_to_remove = current_retailers_hosts - active_retailers_hosts

    for host in retailers_to_remove:
        current_retailers[host]['is_active'] = False

    for host in retailers_to_override:
        current_retailers[host].update(active_retailers[host])

    for host in retailers_to_add:
        current_retailers[host] = active_retailers[host]

    retailers_conf[provider.domain] = current_retailers
    with open(retailers_conf_path, 'w') as fout:
        json.dump(retailers_conf, fout, indent=4)

    click.secho('Updated %s' % retailers_conf_path, color='green')


@api.command()
@click.pass_context
def retailer_versions(ctx):
    provider = ctx.obj['provider']
    retailers = provider.get_retailer_list()

    pool = Pool(len(retailers))
    results = pool.map(get_retailer_version, retailers)

    table = PrettyTable()
    table.field_names = ['codename', 'title', 'version', 'uptime', 'host']
    for result in results:
        table.add_row(result)
    click.echo(table)
