# -*- coding:utf-8 -*-
__author__ = 'jimmy'
__date__ = '2019/2/18'
import yaml
import os
import traceback
import sys
from optparse import OptionParser
import validate_yml
import logging
from functools import wraps


paths = []

version = validate_yml.__version__

logger = logging.getLogger(__name__)


def parse_options():
    """
    Handle command-line options with optparse.OptionParser.

    Return list of arguments, largely for use in `parse_arguments`.
    """

    # Initialize
    parser = OptionParser(usage="validate_yml [options] [file_path1 file_path2...]")

    # Version number (optparse gives you --version but we have to do it
    # ourselves to get -V too. sigh)
    parser.add_option(
        '-V', '--version', '-v',
        action='store_true',
        dest='show_version',
        default=False,
        help="show program's version number and exit"
    )

    parser.add_option(
        '-f', '--file',
        dest='ymlfile',
        action="store_true",
        default=False,
        help="Validate file with suffix with yml or yaml. example 'validate -f file_1 file_2 dir_3 ...'")
    # parser.add_option_group(group)

    # Finalize
    # Return three-tuple of parser + the output from parse_args (opt obj, args)
    opts, args = parser.parse_args()
    return parser, opts, args


def coroutine(func):
    """
    装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def start(*args, **kwargs):
        c = func(*args, **kwargs)
        next(c)
        return c
    return start


f_p = []


def recursive_file(path):
    if os.path.isdir(path):
        parents = os.listdir(path)
        for parent in parents:
            child = os.path.join(path, parent)
            if os.path.isdir(child):
                recursive_file(child)
            elif os.path.isfile(child) and (child.endswith('.yml') or child.endswith('.yaml')):
                f_p.append(child)
    else:
        f_p.append(path)


def recursive():
    while True:
        path = yield
        if path is None:
            break
        if os.path.isdir(path):
            recursive_file(path)
        else:
            f_p.append(path)
    return f_p


# 委派生成器
@coroutine
def grouper():
    while True:
        file_paths = yield from recursive()
        # 启动校验语法生成器
        c = check_yml_syntax()
        c.send(file_paths)


@coroutine
def check_yml_syntax():
    while True:
        files = yield
        for file in files:
            path = os.path.abspath('.')
            abs_path = os.path.join(path, file)
            try:
                with open(abs_path, encoding='utf-8') as f:
                    yaml.load(f)
                    print(file + "  OK")
            except Exception:
                logger.error(traceback.format_exc())
            finally:
                f_p.remove(file)


def file_exist(*args):
    for file in args:
        path = ''
        if os.path.dirname(file):
            pass
        else:
            path = os.path.abspath('.')
        file_path = os.path.join(path, file)

        if os.path.exists(file_path):
            pass
        else:
            logger.error("Could not find any ymlfile! see --help or -h for available options.")
            sys.exit(1)


def main():
    parser, options, arguments = parse_options()
    if options.show_version:
        print("validate_yml %s" % (version,))
        sys.exit(0)
    if options.ymlfile and arguments:
        file_exist(*arguments)
    else:
        logger.error("correct format：\n    validate_yml -f file_path1 file_path2...")
        sys.exit(1)
    for file_path in arguments:
        group = grouper()
        group.send(file_path)
        group.send(None)
        group.close()


if __name__ == "__main__":
    main()
