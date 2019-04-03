from __future__ import print_function
import argparse

from .namepy import name
from .version import __version__


def name_it():
    return 'Name: {}'.format(name())


def main(args=None):
    '''
    Main entry point for the Namepy command-line interface.
    :param args:  Optional command-line arguments
    :return: None
    '''
    if args is None:
        print(name_it())
        exit(0)


    parser = argparse.ArgumentParser(prog='namepy', description='Namepy command-line interface.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=__version__))

    parser.parse_args(args)


if __name__ == '__main__':
    main()
