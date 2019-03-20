# -*- coding: utf-8 -*-
"""Console script for cde."""
import os
import sys
import collections
from pathlib import Path

import click
import git
import git.exc

import cde.config
# import cde.container

CFG = None
repo_sync_result = collections.namedtuple(
    'SyncResult', ['count_push', 'count_pull', 'changed'])


@click.group()
def main():
    global CFG
    CFG = cde.config.load()
    if not cde.config.validate(CFG):
        sys.exit(1)


# @main.command()
# def shell():
#     cm = cde.container.Docker()
#     cm.shell(cfg['image'], cfg['tag'])


@main.group()
def repo():
    pass


def update_repo(repo, target_branch):
    if target_branch:
        try:
            repo.git.checkout(target_branch, '--')
        except git.exc.GitCommandError:
            repo.git.checkout('master', '--')

    remote = f'{repo.active_branch}' + '@{u}'
    count_pull = len(
        list(repo.iter_commits(f'{repo.active_branch}..{remote}')))
    count_push = len(
        list(repo.iter_commits(f'{remote}..{repo.active_branch}')))
    changed = False

    if count_push == 0 and count_pull:
        changed = True
        # TODO, not just assome 'origin' does exist
        repo.remotes['origin'].pull("--rebase")

    return repo_sync_result(count_push, count_pull, changed)


def diff_count(repo):
    """Count the number of local changes"""

    change_types = ('A', 'D', 'R', 'M', 'T')
    diff_index = repo.index.diff(None)

    # TODO Better way to count all changes
    total = 0
    for change_type in change_types:
        change_iterable = diff_index.iter_change_type(change_type)

        for diff in change_iterable:
            total += 1

    return total


@repo.command()
@click.option(
    '--branch',
    help='If specified given branch is checked out in all repos.'
         '  If it does not exist in a repo master is used instead',
    default=None)
@click.option(
    '--master',
    'branch',
    flag_value='master',
    default=False,
    help='shortcut for --branch=master')
@click.option(
    '--verbose',
    help='Shows additional information, like current commit sha',
    default=False,
    is_flag=True)
@click.option(
    '--stash',
    help='Stash changes if the repo is dirty',
    default=False,
    is_flag=True)
@click.option(
    '--exclude',
    help='Explicitly exclude repos from the update',
    multiple=True)
def sync(branch, verbose, stash, exclude):
    for name, repo_cfg in CFG.get('repos', {}).items():
        if name in exclude:
            click.echo('🙈 {} skipped.'.format(name) + '                     ')
            continue

        path = Path('.') / name

        result = repo_sync_result(0, 0, False)
        stashed_changes = None
        prev_branch = None

        if os.path.exists(path):
            # todo check remote URL
            print('▽ {} fetching...'.format(name), end='', flush=True)
            repo = git.Repo(str(path))
            prev_branch = repo.active_branch

            for remote in repo.remotes:
                remote.fetch()
            msg = f'\r▽ {name} fetched, analyzing changes'
            print(msg, end='', flush=True)
            if repo.is_dirty():
                if not stash:
                    click.secho(
                        f'\r✖ {name} dirty, not updating          ', fg='red')
                    continue
                else:
                    stashed_changes = diff_count(repo)
                    repo.git.stash('save', 'cde sync')

            try:
                result = update_repo(repo, branch)
            except TypeError as e:
                click.secho(f'\r✖ {name} ERROR, not updating: {e}', fg='red')
                continue
        else:
            print('▽ {} cloning...'.format(name), end='', flush=True)

            repo = git.Repo.clone_from(repo_cfg['url'], str(path))
            result = repo_sync_result(0, 0, changed=True)

        flags = ''
        # ' ↓·62↑·1|✚'
        # if changed -> BOLD
        out = click.style(f'\r✔ {name}')
        out += f' [{repo.active_branch}'

        if result.count_pull:
            out += f' ↓·{result.count_pull}'
        if result.count_push:
            out += f' ↑·{result.count_push}'

        branch_changed = repo.active_branch != prev_branch
        if stashed_changes is not None:
            if result.changed or branch_changed:
                out += f'📦·{stashed_changes}'
            else:
                # No need to keep the stash if we did not sync anything
                repo.git.stash('pop')

        if result.count_push and result.count_pull:
            out += click.style(' not pulled', bold=True)

        out += ']'

        if verbose:
            out += f'(SHA1: {repo.rev_parse(str(repo.active_branch))})'

        # TODO make something more... sensible with whitespaces
        # click.get_terminal_size()
        click.echo(out + '                     ')


def env_var_name(name):
    name = name.upper().replace('-', '_')
    return name


@main.command()
def env():
    for name, repo in CFG['repos'].items():
        env_var = env_var_name(name)
        print('{}={}'.format(env_var, repo['commit']))


@main.command()
def check():
    import cde.check
    cde.check.main()


@main.group()
def config():
    pass


# @config.command()
# def update():
#     if not CFG.get('repos', {}).get():
#         click.echo(f'no repo {a} not found in .cde.yml')
#         sys.exit(1)

#     CFG['repos'][repo]['commit'] == commit
#     cde.config.dump(CFG)


if __name__ == "__main__":
    main()
