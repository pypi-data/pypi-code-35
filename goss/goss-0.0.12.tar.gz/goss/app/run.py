#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
from goss import __version__
from goss.app import utils
import configparser
import os
import pyperclip

GOSS_CONFIG_HOME = '{}/.config/goss'.format(os.getenv("HOME"))
GOSS_CONFIG_PATH = '{}/config'.format(GOSS_CONFIG_HOME)
GOSS_CREDENTIAL_PATH = '{}/credentials'.format(GOSS_CONFIG_HOME)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__.__version__)
    ctx.exit()

@click.group()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@click.pass_context
def run(ctx):
    '''
    Github Object Storage
    '''
    if not os.path.exists(GOSS_CONFIG_HOME):
        os.mkdir(GOSS_CONFIG_HOME)
    if os.path.exists(GOSS_CREDENTIAL_PATH):
        cred = configparser.ConfigParser()
        cred.read(GOSS_CREDENTIAL_PATH)
        secs = cred.sections()
        if 'default' in secs:
            default_cred = cred['default']
            user = default_cred['user']
            password = default_cred['password']
            ctx.obj = Github(user, password)

def init_credentials_path():
    if not os.path.exists(GOSS_CONFIG_HOME):
        os.mkdir(GOSS_CONFIG_HOME)

    #  if not os.path.exists(GOSS_CREDENTIAL_PATH):
        #  with open(GOSS_CREDENTIAL_PATH, '+w') as f:
            #  f.flush()
            #  f.close()


@run.command()
@click.option('--user', '-u', prompt='Your Github user', help = 'Your Github user')
@click.option('--password', '-p', prompt='Your Github password',
        help = 'Your Github password',hide_input=True)
@click.pass_context
def credentials(ctx, user, password):
    g = ctx.obj
    confirm = click.style('The credentials is exist. Do you want replace it?', fg='red')
    if g and not click.confirm(confirm):
        return
    conf = configparser.ConfigParser()
    conf['default'] = dict(user = user, password = password)

    with open(GOSS_CREDENTIAL_PATH, 'w') as f:
        conf.write(f)
        click.secho('Success!', fg='cyan')

@run.command()
@click.option('--repo', '-r', is_flag = True, help = 'To create repository')
@click.option('--name', '-n', required = True, help = 'Create object name')
@click.option('--orga', '-o', help = 'If want create organization repository. Is required')
@click.pass_context
def create(ctx, repo, name, orga):
    g = ctx.obj
    if not g:
        click.echo('Seems you c')
        ctx.exit()

    if repo:
        click.echo('Begin create repository')
        click.echo('{}\t: https://github.com/{}/{}'.format(
            utils.make_progress_msg('Url'), name, name))
        click.secho('Waiting...', fg='yellow')
        if orga:
            flag, data = g.create_organization_repository(orga, name)
        else:
            flag, data = g.create_repository(name)
        if not flag:
            utils.print_error(data['message'])
            for err in data['errors']:
                utils.print_error('\t' + err['message'])
        else:
            utils.print_success()

@run.command()
@click.argument('name')
@click.argument('value')
@click.pass_context
def config(ctx, name, value):
    print(name, value)
    pass

if __name__ == "__main__":
    run()
    #  credentials()
