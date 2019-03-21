# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
"""Copyright ©  2018 Justin Stout <justin@jstout.us>."""
from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure


def _bootstrap_repo(ctx):
    """Perform initial github checkin if and only if .gitignore exists."""
    if not Path('.gitignore').is_file():
        raise Failure('.gitignore not found')

    remote_url = 'git@github.com:{}/{}.git'.format(ctx.scm.user_name,
                                                   ctx.scm.name)

    ctx.run('git init')
    ctx.run('git add .')
    ctx.run('git commit -m "new project from {}"'.format(ctx.dev.cc_name))
    ctx.run('git remote add origin {}'.format(remote_url))
    ctx.run('git tag -a "v_0.0.0" -m "cookiecutter ref"')


@task
def init(ctx):
    """Initilialize repo (if required) and configure git flow."""
    bootstrap_repo = not Path('/vagrant/.git').is_dir()

    if bootstrap_repo:
        _bootstrap_repo(ctx)

    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix {}'.format(ctx.scm.versiontagprefix))

    if bootstrap_repo:
        ctx.run('git push -u origin master')
        ctx.run('git push -u origin develop')
        ctx.run('git push --tags')


@task(help={'branches': 'branches to push (default all)', 'tags':
            'push tags (default false)'})
def push(ctx, branch='all', tags=False):
    """Push branches and tags to origin."""
    if branch in ('develop', 'all'):
        ctx.run('git push origin develop')

    if branch in ('master', 'all'):
        ctx.run('git push origin master')

    if tags:
        ctx.run('git push --tags')


@task
def status(ctx):
    """Show status of remote branches."""
    ctx.run('git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads')


SCM_TASKS = Collection('scm')
SCM_TASKS.add_task(init)
SCM_TASKS.add_task(push)
SCM_TASKS.add_task(status)
