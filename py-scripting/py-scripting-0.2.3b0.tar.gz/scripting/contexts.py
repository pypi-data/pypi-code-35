#! /usr/bin/env python
import errno
import os
import shutil
import sys
import tempfile

from .prompting import prompt, status
from .termcolors import blue


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class homebrew_hidden(object):

    """Context that temporarily hides the homebrew folders on Mac."""

    def __init__(self, prefix="/usr/local", prompt=False):
        self._prefix = prefix
        self._folders = ("bin", "lib", "include")
        self._folders_hidden = set()
        self._prompt = prompt

    def __enter__(self):
        folders_to_hide = set()
        if sys.platform == "darwin":
            if not self._prompt or prompt("OK to hide homebrew folders"):
                for folder in self._folders:
                    orig = os.path.join(self._prefix, folder)
                    folders_to_hide.add((orig, orig + ".hide"))

        for (orig, hidden) in folders_to_hide:
            try:
                shutil.move(orig, hidden)
            except Exception:
                pass
            else:
                status("moving: {src} -> {dest}".format(src=orig, dest=hidden))
                self._folders_hidden.add((orig, hidden))

    def __exit__(self, ex_type, ex_value, traceback):
        for (orig, hidden) in self._folders_hidden:
            status("moving: {dest} -> {src}".format(src=orig, dest=hidden))
            shutil.move(hidden, orig)


class cd(object):

    """Context that changes to a new directory.

    Examples
    --------
    >>> import os, tempfile
    >>> from scripting.contexts import cd

    Create a temporary directory for testing.

    >>> test_dir = os.path.realpath(tempfile.mkdtemp())

    Withing the context, we're in the new working directory, after exiting
    the context we're back where we started.

    >>> this_dir = os.getcwd()
    >>> with cd(test_dir) as _:
    ...     wdir = os.getcwd()
    >>> test_dir == wdir
    True
    >>> os.getcwd() == this_dir
    True

    If the new working directory does not exists, create it.

    >>> new_dir = os.path.join(test_dir, 'testing.d')
    >>> os.path.exists(new_dir)
    False
    >>> with cd(new_dir) as _:
    ...     wdir = os.getcwd()
    >>> os.path.exists(new_dir)
    True
    >>> wdir == new_dir
    True
    >>> os.getcwd() == this_dir
    True
    """

    def __init__(self, path_to_dir, create=True):
        self._dir = os.path.expanduser(path_to_dir)
        self._create = create

    def __enter__(self):
        self._starting_dir = os.path.abspath(os.getcwd())
        if self._create:
            mkdir_p(self._dir)
        os.chdir(self._dir)

        return os.path.abspath(os.getcwd())

    def __exit__(self, ex_type, ex_value, traceback):
        os.chdir(self._starting_dir)


class cdtemp(object):

    """Context that creates and changes to a temporary directory.

    Examples
    --------
    >>> import os
    >>> from scripting.contexts import cdtemp

    Change to the newly-created temporary directory after entering the
    context. Upon exiting, remove the temporary directory and return to the
    original working directory.

    >>> this_dir = os.getcwd()
    >>> with cdtemp() as tdir:
    ...     wdir = os.getcwd()
    >>> this_dir == os.getcwd()
    True
    >>> os.path.exists(wdir)
    False
    """

    def __init__(self, **kwds):
        self._cleanup = kwds.pop("cleanup", True)
        self._kwds = kwds
        self._tmp_dir = None

    def __enter__(self):
        self._starting_dir = os.path.abspath(os.getcwd())
        self._tmp_dir = tempfile.mkdtemp(**self._kwds)
        os.chdir(self._tmp_dir)
        return os.path.abspath(self._tmp_dir)

    def __exit__(self, ex_type, ex_value, traceback):
        os.chdir(self._starting_dir)
        if self._cleanup:
            shutil.rmtree(self._tmp_dir)


def _reset_env(keep=None, env=None):
    """Reset the current environmt.

    Parameters
    ----------
    keep : list of str
        Names of environment variables to keep.
    env : dict
        Environment variable names/values for the new environment.
    """
    keep = keep or set()

    for key in os.environ.keys():
        if key not in keep:
            del os.environ[key]

    if env is not None:
        os.environ.update(env)


def env_to_str(env=None):
    env = env or os.environ

    lines = []
    keys = list(env.keys())
    keys.sort()
    for key in keys:
        lines.append("{k}={v}".format(k=key, v=env[key]))

    return os.linesep.join(lines)


class setenv(object):

    """Context that sets up a new environment."""

    def __init__(self, env, verbose=False):
        self._env = env
        self._verbose = verbose

    def __enter__(self):
        self._starting_env = os.environ.copy()
        _reset_env(env=self._env)

        if self._verbose:
            status("switching to this environment:")
            print(blue(env_to_str()))

    def __exit__(self, type, value, traceback):
        _reset_env(env=self._starting_env)


class empty_env(setenv):
    def __init__(self, verbose=False):
        env = {
            "PATH": os.pathsep.join(
                ["/usr/bin", "/bin", "/usr/sbin", "/etc", "/usr/lib"]
            )
        }
        super(empty_env, self).__init__(env, verbose=verbose)
