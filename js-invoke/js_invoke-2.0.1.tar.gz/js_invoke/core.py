# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation

"""
Invoke tasks for Python development.

Copyright ©  2018 Justin Stout <justin@jstout.us>

"""
from pathlib import Path

from invoke import task


def _bootstrap_repo(ctx):
    """Bootstrap repo with standard github configuration."""
    remote_url = 'git@github.com:{}/{}.git'.format(ctx.repo.user_name,
                                                   ctx.repo.name)

    ctx.run('git init')
    ctx.run('git add .')
    ctx.run('git commit -m "new project from {}"'.format(ctx.cc_name))
    ctx.run('git remote add origin {}'.format(remote_url))
    ctx.run('git tag -a "v_0.0.0" -m "cookiecutter ref"')


@task
def init_repo(ctx):
    """Initilialize repo (if required) and configure git flow."""
    bootstrap_repo = not Path('/vagrant/.git').is_dir()

    if bootstrap_repo:
        _bootstrap_repo(ctx)

    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix {}'.format(ctx.repo.versiontagprefix))

    if bootstrap_repo:
        ctx.run('git push -u origin master')
        ctx.run('git push -u origin develop')
        ctx.run('git push --tags')
