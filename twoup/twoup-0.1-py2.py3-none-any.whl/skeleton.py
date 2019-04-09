# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = twoup.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging

from twoup import __version__

__author__ = "Anish Mangal"
__copyright__ = "Anish Mangal"
__license__ = "gpl3"

_logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="List page number sequence to print a small folded double sided booklet")
    parser.add_argument(
        "--version",
        action="version",
        version="twoup {ver}".format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="Number of pages in booklet to be printed",
        type=int,
        metavar="INT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def print_page_order(print_string, upper, lower):
    _logger.debug('print_page_order called with args print_string=%s, upper=%d, lower=%d' % (print_string, upper, lower))
    if(lower < upper):
        print_string += str(upper)+','
        print_string += str(lower)+','
        print_string += str(lower+1)+','
        print_string += str(upper-1)+','
        return print_page_order(print_string, upper-2, lower+2)
    else:
        return (print_string[:-1])

def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Main subroutine begins")
    print_string = ''
    if((args.n % 4) == 0):
        print(print_page_order(print_string,args.n,1))
    else:
        _logger.warn("The number of pages in your booklet to be printed two sided must be a multiple of four. eg. 4,8,12...")
    _logger.debug("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
