# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation

"""
Invoke tasks for Python development.

Copyright ©  2018 Justin Stout <justin@jstout.us>

"""
import importlib.util
import os

from invoke import Collection
from invoke import task

from . import tests


def _get_pkg_version(ctx):
    """Extract __version__ from __init__.py."""
    path = 'src/{}/{}/__init__.py'.format(ctx.python.pkg_name, ctx.python.pkg_name)
    spec = importlib.util.spec_from_file_location(ctx.python.pkg_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod.__version__


@task(help={'name': 'major, minor, or hotfix'})
def bump_version(ctx, name):
    """Bump version."""
    name = name if name != 'hotfix' else 'patch'

    path = 'src/{}/{}/__init__.py'.format(ctx.python.pkg_name, ctx.python.pkg_name)
    version = _get_pkg_version(ctx)

    cmd = 'bumpversion --current-version {} {} {}'.format(version, name, path)
    ctx.run(cmd)


@task
def clean(ctx):
    """Clean bytecode."""
    ctx.run('find . | grep __pycache__ | xargs rm -rf')
    ctx.run('find . | grep .pytest_cache | xargs rm -rf')


@task(clean)
def cleaner(ctx):
    """Clean build directories."""
    patterns = ('build',
                'dist',
                'stage',
                'src/{PKG_NAME}/{PKG_NAME}.egg-info'.format(PKG_NAME=ctx.python.pkg_name)
                )

    for pattern in patterns:
        ctx.run('rm -rf {}'.format(pattern))


@task(cleaner)
def cleanest(ctx):
    """Clean tox virt envs."""
    cmd = "rm -rf src/{PKG_NAME}/.tox".format(PKG_NAME=ctx.python.pkg_name)
    ctx.run(cmd)


@task
def install(ctx):
    """Perform editable user install of module."""
    cmd = '/usr/bin/env python3 -m pip install --user -e src/{}'.format(ctx.python.pkg_name)
    ctx.run(cmd)


@task()
def package_distutils(ctx):
    """Build Python wheel and sdist."""
    with ctx.cd('src/{}'.format(ctx.python.pkg_name)):
        ctx.run('python3 setup.py build sdist bdist_wheel')

    patterns = (
        'src/{}/build'.format(ctx.python.pkg_name),
        'src/{}/dist'.format(ctx.python.pkg_name),
        )

    for pattern in patterns:
        ctx.run('mv {} .'.format(pattern))


PYTHON_TASKS = Collection()
PYTHON_TASKS.add_task(bump_version)
PYTHON_TASKS.add_task(clean)
PYTHON_TASKS.add_task(cleaner)
PYTHON_TASKS.add_task(cleanest)
PYTHON_TASKS.add_task(install)

PYTHON_TESTS = Collection()
PYTHON_TESTS.add_task(tests.test_pylint_errors, name='errors')
PYTHON_TESTS.add_task(tests.test_pylint, name='lint')
PYTHON_TESTS.add_task(tests.test_codestyle, name='code-style')
PYTHON_TESTS.add_task(tests.test_docstyle, name='doc-style')
PYTHON_TESTS.add_task(tests.test_unit, name='unit')
PYTHON_TESTS.add_task(tests.test_integration, name='integration')
PYTHON_TESTS.add_task(tests.test_regression, name='regression')
PYTHON_TESTS.add_task(tests.test_tox, name='tox')
PYTHON_TESTS.add_task(tests.test_refactor, name='refactor')
