#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

###################################################################################
#                                                                                 #
# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/               #
# Contact: beat.support@idiap.ch                                                  #
#                                                                                 #
# Redistribution and use in source and binary forms, with or without              #
# modification, are permitted provided that the following conditions are met:     #
#                                                                                 #
# 1. Redistributions of source code must retain the above copyright notice, this  #
# list of conditions and the following disclaimer.                                #
#                                                                                 #
# 2. Redistributions in binary form must reproduce the above copyright notice,    #
# this list of conditions and the following disclaimer in the documentation       #
# and/or other materials provided with the distribution.                          #
#                                                                                 #
# 3. Neither the name of the copyright holder nor the names of its contributors   #
# may be used to endorse or promote products derived from this software without   #
# specific prior written permission.                                              #
#                                                                                 #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED   #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          #
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE    #
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL      #
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR      #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER      #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE   #
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.            #
#                                                                                 #
###################################################################################


import click

from . import common
from .decorators import raise_on_error
from .click_helper import AliasedGroup


@click.group(cls=AliasedGroup)
@click.pass_context
def toolchains(ctx):
    """toolchains commands"""
    pass



@toolchains.command()
@click.option('--remote', help='Only acts on the remote copy of the list.',
              is_flag=True)
@click.pass_context
@raise_on_error
def list(ctx, remote):
    '''Lists all the toolchains available on the platform.

    To list all existing toolchains on your local prefix:

        $ beat toolchains list
    '''
    if remote:
        with common.make_webapi(ctx.meta['config']) as webapi:
            return common.display_remote_list(webapi, 'toolchain')
    else:
        return common.display_local_list(ctx.meta['config'].path, 'toolchain')


@toolchains.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def path(ctx, names):
  '''Displays local path of toolchain files

  Example:
    $ beat toolchains path xxx
  '''
  return common.display_local_path(ctx.meta['config'].path, 'toolchain', names)


@toolchains.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def edit(ctx, name):
  '''Edit local toolchain file

  Example:
    $ beat toolchains edit xxx
  '''
  return common.edit_local_file(ctx.meta['config'].path,
                                ctx.meta['config'].editor, 'toolchain',
                                name)


@toolchains.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def check(ctx, names):
    '''Checks a local toolchain for validity.

    $ beat toolchains check xxx
    '''
    return common.check(ctx.meta['config'].path, 'toolchain', names)



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.pass_context
@raise_on_error
def pull(ctx, names, force):
    '''Downloads the specified toolchains from the server.

       $ beat toolchains pull xxx.
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        status, downloaded = common.pull(
            webapi, ctx.meta['config'].path, 'toolchain', names,
            ['declaration', 'description'], force, indentation=0)
        return status



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--force', help='Performs operation regardless of conflicts',
              is_flag=True)
@click.option('--dry-run', help="Doesn't really perform the task, just "
              "comments what would do", is_flag=True)
@click.pass_context
@raise_on_error
def push(ctx, names, force, dry_run):
    '''Uploads toolchains to the server

    Example:
      $ beat toolchains push --dry-run yyy
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return common.push(
            webapi, ctx.meta['config'].path, 'toolchain', names,
            ['name', 'declaration', 'description'], {}, force, dry_run, 0
        )



@toolchains.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def diff(ctx, name):
    '''Shows changes between the local dataformat and the remote version

    Example:
      $ beat toolchains diff xxx
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return common.diff(webapi, ctx.meta['config'].path, 'toolchain',
                           name, ['declaration', 'description'])



@toolchains.command()
@click.pass_context
@raise_on_error
def status(ctx):
    '''Shows (editing) status for all available toolchains

    Example:
      $ beat toolchains status
    '''
    with common.make_webapi(ctx.meta['config']) as webapi:
        return common.status(webapi, ctx.meta['config'].path, 'toolchain')[0]



@toolchains.command()
@click.argument('names', nargs=-1)
@click.pass_context
@raise_on_error
def create(ctx, names):
    '''Creates a new local toolchain.

    $ beat toolchains create xxx
    '''
    return common.create(ctx.meta['config'].path, 'toolchain', names)



@toolchains.command()
@click.argument('name', nargs=1)
@click.pass_context
@raise_on_error
def version(ctx, name):
    '''Creates a new version of an existing toolchain.

    $ beat toolchains version xxx
    '''
    return common.new_version(ctx.meta['config'].path, 'toolchain', name)



@toolchains.command()
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.pass_context
@raise_on_error
def fork(ctx, src, dst):
    '''Forks a local toolchain.

    $ beat toolchains fork xxx yyy
    '''
    return common.fork(ctx.meta['config'].path, 'toolchain', src, dst)



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--remote', help='Only acts on the remote copy.',
              is_flag=True)
@click.pass_context
@raise_on_error
def rm(ctx, names, remote):
    '''Deletes a local toolchain (unless --remote is specified).

    $ beat toolchains rm xxx
    '''
    if remote:
        with common.make_webapi(ctx.meta['config']) as webapi:
            return common.delete_remote(webapi, 'toolchain', names)
    else:
        return common.delete_local(ctx.meta['config'].path, 'toolchain', names)



@toolchains.command()
@click.argument('names', nargs=-1)
@click.option('--path', help='Use path to write files to disk (instead of the '
              'current directory)', type=click.Path())
@click.pass_context
@raise_on_error
def draw(ctx, names, path):
    '''Creates a visual representation of the toolchain'''
    return common.dot_diagram(
        ctx.meta['config'].path, 'toolchain', names, path, []
    )
