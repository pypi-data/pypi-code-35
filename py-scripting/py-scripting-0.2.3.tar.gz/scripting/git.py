#! /usr/bin/env python
import os

from .contexts import cd
from .unix import check_output, status, system, which


def git_repo_name(url):
    """Get the name of a `git` repository.

    Parameters
    ----------
    url : str
        Repository URL.

    Returns
    -------
    str
        The name of the repository.

    """
    (base, _) = os.path.splitext(os.path.basename(url))
    return base


def git_repo_sha(url, git=None, branch="master"):
    """Get the hash of the latest commit to a `git` repository.

    Parameters
    ----------
    url : str
        Repository URL.
    git : str, optional
        The `git` executable to use (default is None).
    branch : str, optional
        Repository branch to access (default is 'master').

    Returns
    -------
    str
        The first ten characters of the hash key.

    """
    git = git or which("git")

    lines = check_output([git, "ls-remote", url]).strip().split(os.linesep)
    shas = dict()
    for line in lines:
        (sha, name) = line.split()
        shas[name] = sha

    return shas["refs/heads/{branch}".format(branch=branch)][:10]


def git_clone(url, git=None, dir=".", branch="master"):
    """Clone a `git` repository.

    Parameters
    ----------
    url : str
        Repository URL.
    git : str, optional
        The `git` executable to use (default is None).
    dir : str, optional
        Directory in which repo is cloned (default is '.').
    branch : str, optional
        Repository branch to access (default is 'master').

    """
    git = git or which("git")

    with cd(dir):
        system([git, "init", "-q"])
        system([git, "config", "remote.origin.url", url])
        system(
            [
                git,
                "config",
                "remote.origin.fetch",
                "+refs/heads/*:refs/remotes/origin/*",
            ]
        )
        system(
            [
                git,
                "fetch",
                "origin",
                "{branch}:refs/remotes/origin/{branch}".format(branch=branch),
                "-n",
                "--depth=1",
            ]
        )
        system([git, "reset", "--hard", "origin/{branch}".format(branch=branch)])


def git_pull(url, dir=".", branch="master"):
    """Fetch and integrate a `git` repository.

    Parameters
    ----------
    url : str
        Repository URL.
    dir : str, optional
        Directory in which repo is cloned (default is '.').
    branch : str, optional
        Repository branch to access (default is 'master').

    """
    with cd(dir):
        system(["git", "checkout", "-q", branch])
        system(
            [
                "git",
                "pull",
                "origin",
                "-q",
                "refs/heads/{branch}:refs/remotes/origin/{branch}".format(
                    branch=branch
                ),
            ]
        )


def git_clone_or_update(url, dir=".", branch="master"):
    """Clone or update a `git` repository.

    If the repository exists at the given `dir`, then pull changes
    from the remote; otherwise, clone the repository.

    Parameters
    ----------
    url : str
        Repository URL.
    dir : str, optional
        Directory in which repo is cloned (default is '.').
    branch : str, optional
        Repository branch to access (default is 'master').

    """
    if os.path.isdir(os.path.join(dir, ".git")):
        status("Updating %s" % url)
        git_pull(url, dir=dir, branch=branch)
    else:
        status("Cloning %s" % url)
        git_clone(url, dir=dir, branch=branch)
