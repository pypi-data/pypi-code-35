import os
import math
import shlex
import subprocess as s
import uuid

import click


def mean(arr):
    return sum(arr) / len(arr)


@click.group()
def main():
    """Collection of scripts for rebotics"""
    # click.echo("Main group")
    pass


@main.command()
@click.argument('container')
@click.argument('volume')
def fix_pycharm(container, volume):
    with s.Popen(shlex.split("docker ps -a --format '{{.Names}}'"), stdout=s.PIPE) as proc:
        containers = proc.stdout.read().decode('utf-8').split('\n')
        assert container in containers, 'Container should exist'

    # save helpers to the tmp folder
    tmp_folder = '/tmp/helper_folder_%s' % uuid.uuid4()
    os.system(f'docker cp {container}:/opt/.pycharm_helpers {tmp_folder}')

    # assign new container with attached volume
    helper_random_name = 'helper_%s' % uuid.uuid4()
    os.system('docker run -v {targe_volume}:/opt/.pycharm_helpers --name {name} busybox true'.format(
        targe_volume=volume,
        name=helper_random_name,
    ))

    os.system(f'docker cp {tmp_folder} {helper_random_name}:/opt/.pycharm_helpers')

    # Cleanup
    os.system(f'docker rm -f {helper_random_name}')
    os.system(f'rm -rf {tmp_folder}')
    click.echo('Finished')


@main.command()
def fix_pycharm_clean():
    """
    This command fixes all pycharm related volumes and merges the helpers folder to it.
    This is in case when you update pycharm and run with debugger, but it yields error:
    python: can't open file '/opt/.pycharm_helpers/pydev/pydevd.py': [Errno 2] No such file or directory
    :return:
    """
    def find_pycharm_helpers_folders():
        for dirpath, dirnames, filenames in os.walk(os.path.expanduser('~')):
            if 'PyCharm' in dirpath:
                if '/helpers' in dirpath and '/helpers/' not in dirpath:  # get only the top folder
                    if 'pydev' in dirnames:
                        yield dirpath

    helper_folder = ''
    for path in find_pycharm_helpers_folders():
        helper_folder = path
        break
    click.echo(f'Using helper folder: {helper_folder}')

    with s.Popen(shlex.split("docker volume ls --format '{{ .Name }}'"), stdout=s.PIPE) as proc:
        volumes = proc.stdout.read().decode('utf-8').split('\n')

    for volume in volumes:
        if 'helpers' not in volume:
            continue
        click.echo(f'Fixing pycharm_helpers for {volume}')
        # assign new container with attached volume
        container = 'helper_%s' % uuid.uuid4()
        os.system(f'docker run -v {volume}:/opt/.pycharm_helpers --name {container} busybox true')
        os.system(f'docker cp {helper_folder}/. {container}:/opt/.pycharm_helpers/')

        # Cleanup
        os.system(f'docker rm -f {container}')
    click.echo('Finished')


@main.command()
def install_bash_completion():
    path = os.path.expanduser('~/.bashrc')

    with open(path, 'a') as bashrc:
        commands = [
            '# Rebotics scripts autocomplete scripts',
            '# After you uninstall rebotics-scripts, please consider to delete this too',
            'eval "$(_RETAILER_COMPLETE=source retailer)"',
            'eval "$(_ADMIN_COMPLETE=source admin)"',
            'eval "$(_DATASET_COMPLETE=source dataset)"',
            'eval "$(_REBOTICS_COMPLETE=source rebotics)"',
        ]
        for command in commands:
            bashrc.write(command + "\n")

    click.edit(filename=path)
