import json
import os
from datetime import datetime, timezone
from multiprocessing import Pool

import click
import requests
from dateutil import parser as date_parser
from prettytable import PrettyTable
from six.moves.urllib_parse import urlparse

from sdk.providers import RetailerProvider, ProviderHTTPClientException
from sdk.utils import download_file, mkdir_p, \
    get_filename_from_url


class ApiClientException(Exception):
    pass


RETAILER_BASE_URL = None
AUTH_TOKEN = None
USER_ID = None

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'cache-control': 'no-cache',
    'accept-language': 'en-US,en;q=0.9'
}


def is_url(value):
    return urlparse(value).scheme != ''


@click.group()
@click.option('-r', '--retailer')
@click.option('-h', '--host')
@click.option('-u', '--user', prompt=True, )
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.version_option()
@click.pass_context
def api(ctx, retailer, host, user, password):
    """
    This action will login you into retailer that you provide.
    """
    ctx.ensure_object(dict)
    global AUTH_TOKEN, RETAILER_BASE_URL, USER_ID
    if host is None:
        if retailer is None:
            RETAILER_BASE_URL = 'http://china.reboticsdemo.net'
        if retailer:
            response = requests.post('http://admin.rebotics.net/retailers/host/', data={
                'company': retailer
            }).json()
            RETAILER_BASE_URL = response['host']
    else:
        RETAILER_BASE_URL = host
    provider = RetailerProvider(host=RETAILER_BASE_URL, retries=1)
    try:
        provider.api_login(user, password)
        click.echo("Successfully logged in for retailer", err=True)
    except ProviderHTTPClientException:
        raise ProviderHTTPClientException("Failed To login")
    ctx.obj['provider'] = provider


@api.command()
@click.pass_context
def version(ctx):
    provider = ctx.obj['provider']
    click.echo(provider.version())


@api.command()
@click.option('-t', '--input_type')
@click.option('-s', '--store', type=click.INT)
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@click.pass_context
def upload_files(ctx, input_type, store, files):
    provider = ctx.obj['provider']
    file_ids = []
    for f_ in files:
        response = provider.processing_upload(
            store, f_, input_type
        )
        click.echo(response, err=True)  # redirecting this output to stderr
        file_ids.append(response['id'])
    click.echo(' '.join(map(str, file_ids)))


@api.command()
@click.argument('processing_id', type=click.INT, required=True)
@click.pass_context
def requeue(ctx, processing_id):
    provider = ctx.obj['provider']
    response = provider.requeue(processing_id)
    click.echo(response, err=True)
    click.echo(response['id'])


@api.command()
@click.option('-t', '--input_type')
@click.option('-s', '--store', type=click.INT)
@click.option('-p', '--store-planogram', type=click.INT)
@click.option('--aisle')
@click.option('--section')
@click.option('-l', '--lens-used', is_flag=True, default=False)
@click.argument('files', nargs=-1, required=True, type=click.INT)
@click.pass_context
def create_processing_action(ctx, input_type, store, store_planogram, aisle, section, lens_used, files):
    provider = ctx.obj['provider']

    response = provider.create_processing_action(
        store, files, input_type,
        store_planogram=store_planogram,
        aisle=aisle,
        section=section,
        lens_used=lens_used
    )
    click.echo(response, err=True)
    click.echo(response['id'])


def download_file_from_dict(d):
    click.echo('>> Downloading file into %s' % d['filepath'], err=True)
    result = download_file(d['url'], d['filepath'])
    click.echo('<< Downloaded file into %s' % d['filepath'], err=True)
    return result


@api.command()
@click.argument('actions', nargs=-1, required=True, type=click.INT)
@click.option('-t', '--target', type=click.Path(), default='.')
@click.option('-c', '--concurrency', type=int, default=4)
@click.pass_context
def download_processing_action(ctx, actions, target, concurrency):
    provider = ctx.obj['provider']

    pool = Pool(concurrency)
    files_to_download = []

    for action_id in actions:
        processing_action_folder = os.path.join(target, 'ProcessingAction#%d' % action_id)

        click.echo('Get Processing action %s' % action_id, err=True)
        data = provider.processing_action_detail(action_id)
        mkdir_p(processing_action_folder)
        results = os.path.join(processing_action_folder, 'results')
        inputs = os.path.join(processing_action_folder, 'inputs')

        mkdir_p(results)
        mkdir_p(inputs)

        for key in ['merged_image_jpeg', 'merged_image', ]:
            files_to_download.append({
                'url': data[key],
                'filepath': os.path.join(results, get_filename_from_url(data[key]))
            })

        for input_object in data.get('inputs', []):
            files_to_download.append({
                'filepath': os.path.join(get_filename_from_url(input_object['file'])),
                'url': input_object['file']
            })

        with open(os.path.join(processing_action_folder, 'processing_action_%d.json' % action_id), 'w') as fout:
            json.dump(data, fout, indent=4)

        click.echo('Downloading files for %s' % (action_id,), err=True)

    pool = Pool(concurrency)
    pool.map(download_file_from_dict, files_to_download)

    click.echo('Processing download success', err=True)


def upload_preview_task(d):
    provider = d['provider']
    images_path = d['images_path']
    upc = d['upc']
    delete = d['delete']

    if delete:
        try:
            response = provider.delete_product_previews(upc)
            click.echo('Deleted %s previews for product %s' % (response['deleted'], upc, ), err=True)
        except ProviderHTTPClientException:
            click.echo('Product with UPC %s does not exists' % upc, err=True)

    for image_path in images_path:
        with open(image_path, 'rb') as image:
            try:
                response = provider.upload_product_preview(upc, image)
            except ProviderHTTPClientException as e:
                click.echo("xxx Failed to send image: %s" % image_path)
                click.echo(str(e), err=True)
            click.echo('<< Uploaded product preview for %s from %s' % (upc, image_path), err=True)


@api.command()
@click.option('-d', '--delete', is_flag=True)
@click.option('-c', '--concurrency', type=int, default=4)
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
@click.pass_context
def upload_previews_from_folder(ctx, delete, concurrency, path):
    """
    Upload previews from file system to the server in parallel
    It has increased retries
    :param path:
    :return:
    """
    provider = ctx.obj['provider']
    provider.retries = 5

    tasks = []
    for label in os.listdir(path):
        upc_folder = os.path.join(path, label)
        if not os.path.isdir(upc_folder):
            continue

        click.echo('Reading folder: %s' % upc_folder, err=True)
        task = {
            'provider': provider,
            'images_path': [],
            'delete': delete,
            'upc': label
        }

        if label.isdigit():
            for filename in os.listdir(upc_folder):
                image_path = os.path.join(upc_folder, filename)

                if os.path.isfile(image_path):
                    task['images_path'].append(image_path)

        if task['images_path']:
            tasks.append(task)

    click.echo('Number of tasks: {}'.format(len(tasks)), err=True)
    p = Pool(concurrency)
    p.map(upload_preview_task, tasks)
    click.echo('Finished')


@api.command()
@click.option('-s', '--store', type=click.INT)
@click.option('-p', '--page', type=click.INT, default=1)
@click.option('-r', '--page-size', type=click.INT, default=10)
@click.pass_context
def processing_action_table(ctx, store, page, page_size):
    provider = ctx.obj['provider']

    table = PrettyTable()
    table.field_names = ['#', 'id', 'store', 'user', 'status', 'created', 'last_requeue', 'last_requeue ago']
    # TODO: add time in queue
    click.echo('Getting list of processing actions', err=True)
    data = provider.get_processing_action_list(
        store,
        page=page,
        page_size=page_size,
    )
    now = datetime.now(timezone.utc)
    for i, processing_action in enumerate(data):

        created_datetime = date_parser.parse(processing_action['created'])
        last_requeue_datetime = date_parser.parse(processing_action['last_requeue'])

        table.add_row([
            i,
            processing_action['id'],
            '#{store_id} {store_title}'.format(**processing_action),
            '{username}'.format(**processing_action['user']),
            processing_action['status'],
            created_datetime.strftime('%c'),
            last_requeue_datetime.strftime('%c'),
            str(now - last_requeue_datetime)
        ])
    click.echo(table)
