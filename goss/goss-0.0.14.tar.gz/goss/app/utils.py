#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click
import configparser
import os


GOSS_CONFIG_HOME = '{}/.config/goss'.format(os.getenv("HOME"))
GOSS_CONFIG_PATH = '{}/config'.format(GOSS_CONFIG_HOME)
GOSS_CREDENTIAL_PATH = '{}/credentials'.format(GOSS_CONFIG_HOME)

def print_success(msg='Success!'):
    click.secho(msg, fg='cyan')

def print_failed(msg='Failed!'):
    click.secho(msg, fg='red')

def print_progress(msg='Waiting...'):
    click.secho(msg, fg='yellow')

def print_error(msg):
    click.secho(msg, fg='red')

def make_progress_msg(msg):
    return click.style(msg, fg = 'yellow')

def make_error_msg(msg):
    return click.style(msg, fg = 'red')

def config(filepath, section, **data):
    conf = configparser.ConfigParser()
    if os.path.exists(filepath):
        conf.read(filepath)

    conf[section] = data

    with open(filepath, 'w') as f:
        conf.write(f)
        f.close()

