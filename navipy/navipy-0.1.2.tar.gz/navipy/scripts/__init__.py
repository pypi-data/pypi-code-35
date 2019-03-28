"""

"""
import argparse
import logging


def parser_logger(parser=argparse.ArgumentParser()):
    """ Append logger argparse """
    arghelp = 'To display some stuff \n'
    arghelp += ' * -v print command \n'
    arghelp += ' * -vv print also script'
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help=arghelp)

    arghelp = 'Outputfile for logging \n'
    parser.add_argument('--logfile',
                        default=None,
                        help=arghelp)

    return parser


def args_to_logparam(args):
    logfile = args.logfile
    if args.verbose == 1:
        return logging.WARNING, logfile
    elif args.verbose == 2:
        return logging.INFO, logfile
    elif args.verbose >= 3:
        return logging.DEBUG, logfile
    else:
        return logging.ERROR, logfile
