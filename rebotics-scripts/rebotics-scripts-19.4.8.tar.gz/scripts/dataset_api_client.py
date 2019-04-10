import os
import shutil
from multiprocessing.pool import Pool

import click
import requests
from tqdm import tqdm

from sdk.providers import DatasetProvider
from sdk.utils import download_file, mkdir_p


@click.group()
@click.option('-h', '--host', prompt=True)
@click.option('-u', '--user', prompt=True, )
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.version_option()
@click.pass_context
def api(ctx, host, user, password):
    """
    This action will login you into retailer that you provide.
    """
    ctx.ensure_object(dict)

    dataset_provider = DatasetProvider(host, retries=1)
    dataset_provider.token_auth(user, password)
    ctx.obj['provider'] = dataset_provider


def save_image(d):
    download_file(d['url'], d['filepath'])
    click.echo('Downloaded jpeg image to {}'.format(d['filepath']))


@api.command()
@click.argument('meta_data_url',)
@click.option('-t', '--target', type=click.Path(), default='.')
@click.option('-c', '--concurrency', type=int, default=4)
@click.pass_context
def setup_training_dir(ctx, meta_data_url, target, concurrency):
    click.echo("Downloading meta data from {}".format(meta_data_url), err=True)
    response = requests.get(meta_data_url)
    response.raise_for_status()

    meta_data = response.json()
    click.echo("Downloaded meta data from {}".format(meta_data_url), err=True)

    mkdir_p(target)
    annotations_path = os.path.join(target, 'Annotations')
    mkdir_p(annotations_path)
    images_path = os.path.join(target, 'JPEGImages')
    mkdir_p(images_path)
    image_sets_path = os.path.join(target, 'ImageSets')
    mkdir_p(image_sets_path)
    main_path = os.path.join(image_sets_path, 'Main')
    mkdir_p(main_path)

    for file_in_main in meta_data['main']:
        with open(os.path.join(main_path, file_in_main['filename']), 'w') as fout:
            fout.write(file_in_main['value'])

    for annotation_file in meta_data['annotations']:
        with open(os.path.join(annotations_path, annotation_file['filename']), 'w') as fout:
            fout.write(annotation_file['value'])

    click.echo("Saved annotation files. Fetching images...", err=True)

    p = Pool(concurrency)
    jpeg_images = [
        {
            'url': i['url'],
            'filepath': os.path.join(images_path, i['image_name'])
        } for i in meta_data['jpeg_images']
    ]
    p.map(save_image, jpeg_images)


@api.command()
@click.argument('ref_upc', type=click.File())
@click.argument('ref_features', type=click.File())
@click.option('-r', '--retailer', prompt=True, )
@click.option('-f', '--facenet', prompt=True, )
@click.pass_context
def upload_ref(ctx, ref_upc, ref_features, retailer, facenet):
    provider = ctx.obj['provider']

    click.echo('Starting uploading to {provider.host} for {retailer} and {facenet}...'.format(
        provider=provider, retailer=retailer, facenet=facenet
    ), err=True)

    for upc, feature in tqdm(zip(ref_upc, ref_features)):
        data = provider.save_feature_vector(retailer=retailer, facenet=facenet, upc=upc, feature=feature)

    click.echo('Done uploading to {provider.host} for {retailer} and {facenet}!'.format(
        provider=provider, retailer=retailer, facenet=facenet
    ))


@api.command()
@click.option('-r', '--retailer', prompt=True, )
@click.option('-f', '--facenet', prompt=True, )
@click.argument('output', type=click.Path(), default='.')
@click.pass_context
def download_backup(ctx, retailer, facenet, output):
    provider = ctx.obj['provider']
    filename, raw = provider.download_reference_database(retailer, facenet)

    if os.path.isdir(output):
        mkdir_p(output)
        output = os.path.join(output, filename)
    elif os.path.isfile(output):
        mkdir_p(os.path.dirname(output))
    else:
        raise OSError('Could not write to path that does not')

    click.echo(output)
    with open(output, 'wb') as out_file:
        shutil.copyfileobj(raw, out_file)


@api.command()
def ping():
    pass
