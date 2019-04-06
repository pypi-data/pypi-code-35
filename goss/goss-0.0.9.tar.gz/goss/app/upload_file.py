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
    #  g = Github()
    click.echo('Begin upload\t: {}'.format(filepath))
    click.echo('Create to\t: https://github.com/{}/{}'.format(owner, repo))
    res = github.create_from_file(owner, repo, filepath, path)
    res.contents
    cont = res.contents[0]

    click.echo('Success!')
    click.echo('The download url is\n\n\t{}\n\nYou can use it by <ctrl-v>'.format(cont.download_url))
    pyperclip.copy(cont.download_url)

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
