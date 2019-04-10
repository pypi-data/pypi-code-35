#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
from goss import Github
from goss import __version__
from goss.app import utils
from goss.app.logger import Logger
import configparser
import os
import pyperclip
import json

GOSS_CONFIG_HOME = '{}/.config/goss'.format(os.getenv("HOME"))
GOSS_CONFIG_PATH = '{}/config'.format(GOSS_CONFIG_HOME)
GOSS_CREDENTIAL_PATH = '{}/credentials'.format(GOSS_CONFIG_HOME)
GOSS_USER_INFO_PATH = '{}/user.json'.format(GOSS_CONFIG_HOME)

logger = Logger()

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

            g = Github(user, password)
            g.set_owner(default_cred['owner'])
            ctx.obj = g

def init_credentials_path():
    if not os.path.exists(GOSS_CONFIG_HOME):
        os.mkdir(GOSS_CONFIG_HOME)

    #  if not os.path.exists(GOSS_CREDENTIAL_PATH):
        #  with open(GOSS_CREDENTIAL_PATH, '+w') as f:
            #  f.flush()
            #  f.close()


@run.command(help='Log in to the github account')
@click.option('--user', '-u', prompt='Your Github user', help = 'Your Github user')
@click.option('--password', '-p', prompt='Your Github password',
        help = 'Your Github password',hide_input=True)
@click.option('--yes', '-y', is_flag = True, default = False, help = 'All questions answered yes')
@click.pass_context
def login(ctx, user, password, yes):
    g = ctx.obj
    confirm = utils.make_error_msg('The login information already exists. Do you want to replace it?')
    if not yes:
        if g and not click.confirm(confirm):
            return
    conf = configparser.ConfigParser()
    conf['default'] = dict(user = user, password = password)

    g = Github(user, password)
    code, data = g.get_user_info()
    if code != 200:
        utils.print_failed()
        logger.error('用户名或密码错误')
        return

    owner = data.get("name")
    conf['default']['owner'] = owner
    with open(GOSS_CREDENTIAL_PATH, 'w') as f:
        conf.write(f)
    with open(GOSS_USER_INFO_PATH, 'w') as f:
        f.write(json.dumps(data, indent = 4))
        f.flush()
        f.close()

    conf_data = dict(name = owner)
    email = data.get("email")
    if email:
        conf_data['email'] = email

    utils.config(GOSS_CONFIG_PATH, 'user', **conf_data)

    utils.print_success()
    logger.info('Name  :', owner)
    logger.info('Email :', email)


#  @run.command()
#  @click.option('--repo', '-r', is_flag = True, help = 'To create repository')
#  @click.option('--name', '-n', required = True, help = 'Create object name')
#  @click.option('--orga', '-o', help = 'If want create organization repository. Is required')
#  @click.pass_context
#  def create(ctx, repo, name, orga):
    #  g = ctx.obj
    #  if not g:
        #  click.echo('You have not logged in yet, please go to goss-cli login to login')
        #  click.echo('You have not logged in yet, please go to goss-cli login to login')
        #  click.echo('You have not logged in yet, please go to goss-cli login to login')
        #  ctx.exit()
    #  if repo:
        #  click.echo('Begin create repository')
        #  click.echo('{}\t: https://github.com/{}/{}'.format(
            #  utils.make_progress_msg('Url'), name, name))
        #  click.secho('Waiting...', fg='yellow')
        #  if orga:
            #  flag, data = g.create_organization_repository(orga, name)
        #  else:
            #  flag, data = g.create_repository(name)
        #  if not flag:
            #  utils.print_error(data['message'])
            #  for err in data['errors']:
                #  utils.print_error('\t' + err['message'])
        #  else:
            #  utils.print_success()

@run.command()
@click.option('--method', '-m', default = 'GET',
    help = 'GET/POST/PUT/DELETE for repository. Default is GET')
@click.option('--orga', '-o', help = 'If want create organization repository. Is required')
@click.argument('name', required = False)
@click.pass_context
def repo(ctx, name, orga, method):
    '''
    Get/Create your repositorys
    '''
    g = ctx.obj
    if not g:
        click.echo('You have not logged in yet, please run goss-cli to login')
        ctx.exit()

    owner = orga if orga else g.owner

    def print_repo_detail(r):
        '''打印单个 repository'''
        #  click.secho('*' * 60, fg='yellow')
        id_text = click.style('Id', fg='red')
        click.echo('{}     : {}'.format(utils.make_error_msg('Id'), r['id']))
        click.echo('{}   : {}'.format(utils.make_error_msg('Name'), r['name']))
        click.echo('{}  : {}'.format(utils.make_error_msg('Owner'),
            r['owner']['login']))
        click.echo('{}    : {}'.format(utils.make_error_msg('Url'),
            r['html_url']))
        click.echo('{}   : {}'.format(utils.make_error_msg('Desc'),
            r['description']))
        #  click.echo('{} : {}'.format('Detail', r['url']))
        click.echo('More details see: {}'.format(click.style(r['url'], fg='blue')))
        #  click.secho('*' * 60, fg='yellow')

    method = method.lower()
    if method == 'get':     # 处理 get 请求
        if name:            # 获取单个 repository
            logger.info('Query repository {}/{}'.format(owner, name))
            logger.info('Waiting...')
            code, repo = g.get_repository(owner, name)
            if code != 200:
                utils.print_failed()
                logger.error(repo.get("message"))
                ctx.exit()
            print_repo_detail(repo)
            utils.print_success()
            ctx.exit()

        # 获取全部 repositorys
        logger.info('Query your repositorys.')
        logger.info('Waiting...')
        code, repos = g.get_owner_repositorys()
        click.secho('id\tname\tfull_name\turl', fg='cyan')
        click.secho('-' * 60, fg='yellow')
        for r in repos:
            click.echo('{}\t{}\t{}\t{}'.format(r['id'], r['name'],
                r['full_name'], r['html_url']))
        click.secho('-' * 60, fg='yellow')
        click.secho('Total : {}'.format(len(repos)))
        ctx.exit()
    elif method == 'post':
        logger.info("Create repository")
        logger.info("Url : https://github.com/{}/{}".format(owner, name))
        logger.info('Waiting...')
        code, data = g.create_repository(name)
        if code == 201:
            utils.print_success()
        else:
            utils.print_failed()
            logger.error(data.get("message"))
    elif method == 'delete':
        logger.info("Delete repository")
        logger.info("Url : https://github.com/{}/{}".format(owner, name))
        logger.info('Waiting...')
        code, data = g.delete_repository(owner, name)
        if code == 204:
            utils.print_success()
        else:
            utils.print_failed()
            logger.error(data.get("message"))



    #  if repo:
        #  click.echo('Begin create repository')
        #  click.echo('{}\t: https://github.com/{}/{}'.format(
            #  utils.make_progress_msg('Url'), name, name))
        #  click.secho('Waiting...', fg='yellow')
        #  if orga:
            #  flag, data = g.create_organization_repository(orga, name)
        #  else:
            #  flag, data = g.create_repository(name)
        #  if not flag:
            #  utils.print_error(data['message'])
            #  for err in data['errors']:
                #  utils.print_error('\t' + err['message'])
        #  else:
            #  utils.print_success()

@run.command()
@click.argument('name', required = False)
@click.argument('value', required = False)
@click.pass_context
def config(ctx, name, value):
    '''
    Get/Create/Update goss config
    '''
    if name and value and '.' in name:
        names = name.split('.')
        section = names[0]
        key = names[1]
        utils.config(GOSS_CONFIG_PATH, section, **{key: value})
        utils.print_success()
        return

    conf = configparser.ConfigParser()
    conf.read(GOSS_CONFIG_PATH)
    secs = conf.sections()
    for sec in secs:
        click.echo('[{}]'.format(sec))
        kv = conf[sec]
        for k, v in kv.items():
            click.echo('    {} = {}'.format(k, v))


if __name__ == "__main__":
    run()
    #  credentials()
