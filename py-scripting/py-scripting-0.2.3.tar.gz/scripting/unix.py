#! /usr/bin/env python
from __future__ import print_function

import glob
import os
import platform
import re
import shutil
import subprocess
import sys

from .contexts import cd
from .prompting import error, status


def is_linux():
    """Check if machine is linux."""
    return platform.system() == "Linux"


def is_osx():
    """Check if machine is OSX."""
    return platform.system() == "Darwin"


def is_unix():
    """Check if machine is either Linux or OSX."""
    return is_linux() or is_osx()


def is_executable(prog):
    """Check if a program is executable.

    Parameters
    ----------
    prog : str
        Name of the program to test.

    Returns
    -------
    bool
        True if the program is executable.

    """
    return os.path.isfile(prog) and os.access(prog, os.X_OK)


def check_output(*args, **kwds):
    kwds.setdefault("stdout", subprocess.PIPE)
    return subprocess.Popen(*args, **kwds).communicate()[0]


def system(*args, **kwds):
    verbose = kwds.pop("verbose", True)
    kwds.setdefault("stdout", sys.stderr)

    status(" ".join(args[0]))

    if verbose:
        call = subprocess.check_call
    else:
        call = check_output

    try:
        call(*args, **kwds)
    except subprocess.CalledProcessError:
        error("Unable to run command: {cmd}".format(cmd=" ".join(args[0])))
        raise


def which(prog, env=None):
    """Find path to a program.

    Parameters
    ----------
    prog : str
        Name of the program to search for.
    env : str
        Name of an environment variable that contains the program's path.
    """
    prog = os.environ.get(env or prog.upper(), prog)

    try:
        prog = subprocess.check_output(
            ["which", prog], stderr=open("/dev/null", "w")
        ).strip()
    except subprocess.CalledProcessError:
        return None
    else:
        return prog


def checksum(path):
    import hashlib

    hasher = hashlib.md5()
    with open(path, "r") as contents:
        hasher.update(contents.read())

    return hasher.hexdigest()


def wc_l(fname, with_wc="wc"):
    """Count the lines in a file.

    Parameters
    ----------
    fname : str
        File name.
    with_wc : str, optional
        The 'wc' command to use (default is `wc`).

    Returns
    -------
    int
        Number of lines in file, or None on error.

    """
    try:
        n_lines = subprocess.check_output([with_wc, "-l", fname])
    except Exception:
        raise
    else:
        return int(n_lines.split()[0])


def sensible_name_sort(names):
    """Sort names with numbers in counting order.

    Parameters
    ----------
    names : iterable of str
        Names to sort.

    Returns
    -------
    iterable of str
        Sort names.

    Examples
    --------
    >>> from scripting.unix import sensible_name_sort
    >>> sensible_name_sort(['file1.txt', 'file10.txt', 'file2.txt'])
    ['file1.txt', 'file2.txt', 'file10.txt']
    """
    REGEX = r"(?P<prefix>[\D]*)(?P<num>[\d]*)(?P<suffix>[\D]*)"
    p = re.compile(REGEX)

    keys = []
    for name in names:
        m = p.match(name)
        try:
            key = int(m.group("num"))
        except ValueError:
            key = 0
        finally:
            keys.append((key, name))

    keys.sort()
    return [key[1] for key in keys]


def tail(fname, n=10, with_tail="tail"):
    """Get the last lines in a file.

    Parameters
    ----------
    fname : str
        File name.
    n : int, optional
        Number of lines to get (default is 10).
    with_tail : str, optional
        The 'tail' command to use (default is `tail`).

    Returns
    -------
    str
        The last lines in file, or None on error.

    """
    fname = os.path.abspath(fname)
    try:
        lines = subprocess.check_output([with_tail, "-n{n}".format(n=n), fname])
    except subprocess.CalledProcessError:
        raise RuntimeError("Unable to get status. Please try again.")
    except Exception:
        raise
    else:
        return lines.strip()


def hostname():
    """Get the name of the host system.

    Returns
    -------
    str
        The domain name of the current host.

    """
    import socket

    return socket.getfqdn()


def glob_cp(pattern, dest):
    if not os.path.isdir(dest):
        raise ValueError("{dest}: not a directory".format(dest=dest))

    for fname in glob.glob(pattern):
        status("cp {src} {dest}".format(src=fname, dest=dest))
        shutil.copy2(fname, dest)


def cp(source, dest, dry_run=False, clobber=True, create_dirs=False, silent=False):
    """Copy file from source to destination.

    Parameters
    ----------
    source : str
        Path to source file.
    dest : str
        Path to destination directory or destination file name.
    dry_run : bool, optional
        Print what would have been done, but don't do it.
    clobber : bool, optional
        If destination file exists, overwrite it. Otherwise raise
        an exception.
    create_dirs : bool, optional
        Create intermediate directories if they don't already exist.
        Otherwise, raise an exception if a destination directory is
        missing.
    silent : bool, optional
        Supress displaying anything, except if ``dry_run`` is used.
    """
    cp_args = (source, dest)

    if not silent or dry_run:
        status("cp {0} {1}".format(*cp_args))

    if not dry_run:
        if os.path.isfile(dest) and not clobber:
            raise OSError("{0}: file exists".format(dest))
        elif os.path.islink(dest):
            os.remove(dest)

        with cd(os.path.dirname(dest) or ".", create=create_dirs):
            pass
        shutil.copy2(*cp_args)


def ln_s(source, dest, dry_run=False, clobber=True, create_dirs=False, silent=False):
    """Link file from source to destination.

    Parameters
    ----------
    source : str
        Path to source file.
    dest : str
        Path to destination directory or destination file name.
    dry_run : bool, optional
        Print what would have been done, but don't do it.
    clobber : bool, optional
        If destination file exists, overwrite it. Otherwise raise
        an exception.
    create_dirs : bool, optional
        Create intermediate directories if they don't already exist.
        Otherwise, raise an exception if a destination directory is
        missing.
    silent : bool, optional
        Supress displaying anything, except if ``dry_run`` is used.
    """
    ln_args = (source, dest)

    if not silent or dry_run:
        status("ln -s {0} {1}".format(*ln_args))

    if not dry_run:
        if os.path.isfile(dest):
            if clobber:
                os.remove(dest)
            else:
                raise OSError("{0}: file exists".format(dest))

        with cd(os.path.dirname(dest) or ".", create=create_dirs):
            pass
        os.symlink(*ln_args)
