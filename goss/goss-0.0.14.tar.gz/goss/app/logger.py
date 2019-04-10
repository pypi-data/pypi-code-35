#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
# Description:

import click

class Logger():
    def __init__(self, *args, **kwargs):
        pass

    def info(self, *msg):
        message = ' '.join(msg)
        click.echo(click.style('[INFO] ', fg='yellow') + message)

    def error(self, *msg, with_color=False):
        message = ' '.join(msg)
        if with_color:
            message = click.style(message, fg='red')
        click.echo(click.style('[EROR] ', fg='red') + message)

    def warn(self, *msg, with_color=False):
        message = ' '.join(msg)
        if with_color:
            message = click.style(message, fg='red')
        click.echo(click.style('[WARN] ', fg='red') + message)


