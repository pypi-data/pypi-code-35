#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
import re
from importlib import import_module
import os
from shutil import ignore_patterns, copy2, copystat
import argparse
from pyfiglet import figlet_format
import six

try:
    from termcolor import colored
except ImportError:
    colored = None


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def _is_valid_name(project_name):
    def _module_exists(module_name):
        try:
            import_module(module_name)
            return True
        except ImportError:
            return False

    if not re.search(r'^[_a-zA-Z]\w*$', project_name):
        print('Error: Project names must begin with a letter and contain' +
              ' only\nletters, numbers and underscores')
    elif _module_exists(project_name):
        print('Error: Module %r already exists' % project_name)
    else:
        return True
    return False


def _copytree(src, dst):
    ignore = ignore_patterns('*.pyc', '.svn', '__pycache__')
    names = os.listdir(src)
    ignored_names = ignore(src, names)

    if not os.path.exists(dst):
        os.makedirs(dst)

    for name in names:
        if name in ignored_names:
            continue

        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isdir(srcname):
            _copytree(srcname, dstname)
        else:
            copy2(srcname, dstname)
    copystat(src, dst)


def _arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('framework_name', help='choose a deep learning framework <tensorflow|pytorch|keras>',
                        choices=['tensorflow', 'pytorch', 'keras'])
    parser.add_argument('project_name', help='set your project name')
    args = parser.parse_args()
    return args.framework_name, args.project_name


def run():
    log('DLCreator', color="blue", figlet=True)
    framework_name, project_name = _arg_parse()
    if not _is_valid_name(project_name):
        exit(1)
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    _copytree(os.path.join(templates_dir, framework_name), project_name)
    log('Done! "cd {}" and enjoy!'.format(project_name), color="green")
