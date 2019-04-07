#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
from goss.app import utils
import configparser
import os
import pyperclip

github = None
owner = None
repo = None

GOSS_CONFIG_HOME = '{}/.config/goss'.format(os.getenv("HOME"))
GOSS_CONFIG_PATH = '{}/config'.format(GOSS_CONFIG_HOME)
GOSS_CREDENTIAL_PATH = '{}/credentials'.format(GOSS_CONFIG_HOME)

def init_git_config():
    '''初始化 git 信息'''
    #  if not os.path.exists(GOSS_CONFIG_HOME):
        #  os.mkdir(GOSS_CONFIG_HOME)
    credential_path = GOSS_CREDENTIAL_PATH

    config_path = GOSS_CONFIG_PATH

    if not os.path.exists(GOSS_CREDENTIAL_PATH):
        return None, ''

    credential = configparser.ConfigParser()
    credential.read(credential_path)
    default_cred = credential['default']

    g = Github(default_cred['user'], default_cred['password'])

    config = configparser.ConfigParser()
    config.read(config_path)
    author = config['user']
    g.set_author(author['name'], author['email'])

    return g

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

def create(filepath, path=None, repo=None, yes=False):
    '''
    创建文件
    '''
    if not path:
        path = os.path.basename(filepath)

    config = configparser.ConfigParser()
    config.read(GOSS_CONFIG_PATH)
    if not repo:
        repo = config['repository']['repo']
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
    utils.print_progress()
    g = init_git_config()
    code, data = g.create_from_file(owner, repo, filepath, path)

    if code == 422 and data.get("message") == \
            'Invalid request.\n\n"sha" wasn\'t supplied.':
        if not yes:
            if not click.confirm('This file is exists. Do you want tu replace?'):
                return
        else:
            click.echo('{} {}'.format(
                utils.make_error_msg('Waring!'),
                utils.make_progress_msg('This file is exists. And now replace it.')
                    ))

        utils.print_progress()
        code, data = g.get_file(owner, repo, path)
        sha = data['sha']
        code, data = g.create_from_file(owner, repo, filepath, path, sha)

        if code != 200:
            utils.print_error(data['message'])
            return
    utils.print_success()

@click.command()
@click.option('-u', '--user', help='Github user')
#  @click.option('--owner', help='Github repository owner')
@click.option('--repo', '-r', help='Github repository name')
@click.option('--path', help='Github repository file path')
@click.option('--yes', '-y', is_flag = True, default = False, help='Is anwer yes?')
@click.argument('filepath', type=click.Path(exists=True))
#  @click.confirmation_option(prompt='Are you sure you want to drop the db?')
def run(filepath, user, path, repo, yes):
    '''
    Github Object Storage
    '''
    generate_github()

    create(filepath, path, repo, yes)
    pass

if __name__ == "__main__":
    run()
