#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click

def print_success(msg='Success!'):
    click.secho(msg, fg='cyan')

def print_progress(msg='Waiting...'):
    click.secho(msg, fg='yellow')

def print_error(msg):
    click.secho(msg, fg='red')

def make_progress_msg(msg):
    return click.style(msg, fg = 'yellow')

def make_error_msg(msg):
    return click.style(msg, fg = 'red')
