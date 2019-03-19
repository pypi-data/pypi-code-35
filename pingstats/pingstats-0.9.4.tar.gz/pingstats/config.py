""" Provides ease of use configuration capabilities to the project.

Parses files with arguments for the project split line by line, such that:

    -l droppedstatus,averagepane,rawstatus

Would be appended onto the end of sys.argv.

.. warning:: The config files do not accept the setting of targets

For *Nix users, the project searches for configuration files under the following
paths:
::

    ~/.pingstats.rc

For NT users, the project searches for configuration files under the following
paths:
::

    %LOCALAPPDATA%\\Pingstats\\pingstats.rc
"""
from os import environ, path, access, mkdir, name, F_OK
import sys


if name == 'nt':
    if not access(path.join(environ['LOCALAPPDATA'], 'Pingstats'), F_OK):
        mkdir(path.join(environ['LOCALAPPDATA'], 'Pingstats'))

path = (path.join(environ['LOCALAPPDATA'], 'Pingstats', 'pingstats.rc')
        if name == 'nt' else
        path.join(environ['HOME'], '.pingstats.rc'))


def get_lines():
    """ Returns lines from pingstats.rc if lines exist, or None """
    if access(path, F_OK):
        with open(path) as rc_file:
            return rc_file.readlines()
    else:
        return None


def parse_lines(lines):
    """ Parses lines from pingstats.rc and returns them in  sys.argv compliant
    format """

    for line in lines:
        args = line.strip('\n').split(' ')
        assert len(args) > 1, 'Can not specify default target with rc file'
        yield args


def append_argv(parser):
    """ Appends arguments to sys.argv if those arguments do not already exist """
    for args in parser:
        if not sys.argv.count(args[0]):
            for arg in args:
                sys.argv.append(arg)

        return(sys.argv)

if __name__ == '__main__':
    lines = get_lines()
    if lines is not None:
        try:
            print(append_argv(parse_lines(lines)))
        except AssertionError as e:
            print(str(e))
            exit(1)
