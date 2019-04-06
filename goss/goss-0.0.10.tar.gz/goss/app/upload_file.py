#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
import configparser
import os
import pyperclip

github = None
owner = None
repo = None

def generate_github():
    config_path = '{}/.config/gos/config'.format(os.getenv("HOME"))
    credential_path = '{}/.config/gos/credentials'.format(os.getenv("HOME"))

    credential = configparser.ConfigParser()
    credential.read(credential_path)
    default_cred = credential['default']

    global github
    if not github:
        github = Github(default_cred['user'], default_cred['password'])

    config = configparser.ConfigParser()
    config.read(config_path)
    author = config['user']
    github.set_author(author['name'], author['email'])

    global owner
    global repo
    owner = config['repository']['owner']
    repo = config['repository']['repo']

def create(filepath, path=None):
    '''
    创建文件
    '''
    if not path:
        path = os.path.basename(filepath)
    click.echo('{}\t\t: {}'.format(click.style('Upload', fg='yellow'), filepath))
    click.echo('{}\t\t: https://github.com/{}/{}/{}'.format(
        click.style("To", fg='yellow'),
        owner, repo, path))
    download_url = 'https://raw.githubusercontent.com/{}/{}/master/{}'.format(
        owner, repo, path
    )
    pyperclip.copy(download_url)
    click.echo('{}\t: {}'.format(
        click.style('Download url', fg='yellow'),
        click.style(download_url, fg='blue'),
    ))
    click.echo('Now you can use it in content with {}. Wait upload success it will be avaible'.format(
        click.style('<Ctrl-v>', fg='blue')
    ))
    res = github.create_from_file(owner, repo, filepath, path)
    res.contents
    cont = res.contents[0]

    click.secho('Success!', fg='cyan')

@click.command()
@click.option('-u', '--user', help='Github user')
#  @click.option('--owner', help='Github repository owner')
#  @click.option('--repo', help='Github repository name')
@click.option('--path', help='Github repository file path')
@click.argument('filepath', type=click.Path(exists=True))
def run(filepath, user, path):
    '''
    Github Object Storage
    '''
    generate_github()
    create(filepath, path)
    pass

if __name__ == "__main__":
    run()
