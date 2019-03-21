# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation

"""
Invoke tasks for Python development.

Copyright ©  2018 Justin Stout <justin@jstout.us>

"""
from pathlib import Path

from invoke import task


@task(help={'name': 'major, minor, patch, or increment'})
def bump_version(ctx, mode):
    """Increment version number. Mode: major, minor, patch, increment."""
    idx = {
        'major': 1,
        'minor': 2,
        'patch': 3,
        'increment': 4
        }

    version_file = Path(ctx.ppa.apk.version_file)
    with version_file.open() as fd_in:
        current_version = fd_in.readline().strip()

    ver_parts = list(map(int, current_version.split('.')))[:idx[mode]]
    ver_parts[-1] += 1
    ver_parts.extend([0] * (4 - idx[mode]))

    new_version = '.'.join(map(str, ver_parts))

    with version_file.open('w') as fd_out:
        fd_out.write('{}\n'.format(new_version))
