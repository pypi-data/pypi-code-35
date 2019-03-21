# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
"""Copyright ©  2018 Justin Stout <justin@jstout.us>."""
import os
import platform
import shutil

from pathlib import Path

from invoke import task


@task(help={'branch': 'repo branch: develop, staging, stable'})
def alpine(ctx, branch):
    """Copy package to /data/repo."""
    arch = platform.machine()
    dist_dir = Path('dist')
    repo = Path(ctx.ppa.apk.url) / branch / arch

    os.makedirs(str(repo), exist_ok=True)

    src = list(dist_dir.glob('*.apk'))[0]

    pkg_name = src.stem[:src.stem.rfind(platform.machine())-1].replace('_', '-')
    pkg_name += src.suffix

    dst = Path(repo) / pkg_name

    shutil.copyfile(str(src), str(dst))

    idx_file = repo / 'APKINDEX.tar.gz'
    key_file = Path(ctx.ppa.apk.key_file)

    ctx.run('apk index -o {} {}/*.apk'.format(idx_file, repo))
    ctx.run('abuild-sign -k {} {}'.format(key_file, idx_file))


@task()
def twine(ctx, username, password, repo_url=None):
    """Upload build files to pypi or devpi archive."""
    os.environ['TWINE_USERNAME'] = username
    os.environ['TWINE_PASSWORD'] = password

    if repo_url:
        os.environ['TWINE_REPOSITORY_URL'] = repo_url

    dist_dir = Path('src/{}/dist'.format(ctx.app.pkg_name))
    cmd = 'twine upload {}/*'.format(dist_dir)
    ctx.run(cmd)
