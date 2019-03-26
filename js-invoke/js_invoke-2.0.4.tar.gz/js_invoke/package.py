# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation
"""Copyright ©  2018 Justin Stout <justin@jstout.us>."""
import os
import platform
import shutil

from pathlib import Path

from invoke import task


def _get_dirs(root):
    dirs = []

    for child in Path(root).iterdir():
        if child.is_dir():
            dirs.append(child)
            dirs.extend(_get_dirs(child))

    return dirs


def _get_fpm_depends():
    deps = []

    with open('src/fpm/dependencies.txt', 'r') as fd_in:
        for line in fd_in:
            if line:
                deps.append(
                    '--depends {}'.format(line.strip())
                    )

    return deps


def _get_fpm_scripts():
    scripts = []

    before_install_sh = Path('src/fpm/scripts/before_install.sh')
    after_install_sh = Path('src/fpm/scripts/after_install.sh')

    if before_install_sh.is_file():
        scripts.append(
            '--before-install {}'.format(before_install_sh)
            )

    if after_install_sh.is_file():
        scripts.append(
            '--after-install {}'.format(after_install_sh)
            )

    return scripts


def _get_version(ctx):
    version_file = Path(ctx.ppa.apk.version_file)

    with version_file.open() as fd_in:
        ver_str = fd_in.readline().strip()

    version = ver_str[:ver_str.rfind('.')]
    increment = ver_str[ver_str.rfind('.') + 1:]

    return (version, increment)


def _prune_fpm_build_dir():
    """Delete all .keep files and empty directories."""
    for _file in Path('build/fpm').glob('**/.keep'):
        _file.unlink()

    dirs = _get_dirs('build/fpm')
    dirs.sort(reverse=True)

    for _dir in dirs:
        try:
            _dir.rmdir()

        except OSError:
            # dir not empty
            pass


@task
def fpm(ctx):
    """Create package using FPM."""
    os.makedirs('dist')

    shutil.copytree('src/fpm/root', 'build/fpm')

    if Path('build/bin/').is_dir():
        ctx.run('cp build/bin/* build/fpm/usr/local/bin')

    _prune_fpm_build_dir()

    version, increment = _get_version(ctx)

    options = [
        '--name {}'.format(ctx.fpm.name),
        '--architecture {}'.format(platform.machine()),
        '--chdir build/fpm',
        '--package dist',
        '--input-type dir',
        '--output-type apk',
        '--version {}'.format(version),
        '--iteration r{}'.format(increment)
        ]

    options.extend(_get_fpm_depends())
    options.extend(_get_fpm_scripts())

    cmd = 'fpm {}'.format(' '.join(options))

    ctx.run(cmd)
