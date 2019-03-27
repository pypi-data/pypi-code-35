import argparse
import importlib.util
import logging
from logging.handlers import TimedRotatingFileHandler
import os

from art import text2art

from . import config as default_config
from .data import check_data_version, load_data
from .server import runserver
from .util import EasyDict

name = "ip2loc_server"

CONFIG = EasyDict(LOGGING=None, PATH=None, SERVER=None)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='ip2loc', description='IPV4 2 Geo Location Server')

    parser.add_argument('--config', help=f'Configure file, by default: {default_config.__file__}',
                        default=default_config.__file__)

    parser.add_argument('--showpath', help='show path info', action='store_const', const=True, default=False)

    load_data_arg_group = parser.add_argument_group('Load Data', 'Load data from .csv to database')
    load_data_arg_group.add_argument('--loaddata', action='store_const', const=True, default=False)
    load_data_arg_group.add_argument('--dataver', help='data current version', default=None)
    load_data_arg_group.add_argument('--csv', help='csv file location', default=None)
    load_data_arg_group.add_argument('--zip', help='zip file location', default=None)

    runserver_arg_group = parser.add_argument_group('Runserver', 'Start server')
    runserver_arg_group.add_argument('--runserver', help='default action', action='store_const', const=True, default=False)  # noqa

    return parser.parse_args()


def load_config(config_path_name: str):
    """ Load configs from {config_path_name} to variable 'CONFIG'
    Side effect: revise global variable 'CONFIG'
    """
    spec = importlib.util.spec_from_file_location('config', config_path_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    global CONFIG
    if not os.path.isfile(module.LOG_FILE_PATH):
        log_file_loc = os.path.join(module.LOG_FILE_PATH, 'ip2loc.log')
    else:  # its a file in config
        log_file_loc = module.LOG_FILE_PATH
    CONFIG.LOGGING = EasyDict(
        LOG_LEVEL=module.LOG_LEVEL, LOG_FILE_LOC=log_file_loc, LOG_FORMAT=module.LOG_FORMAT)
    CONFIG.PATH = EasyDict(
        RAW_CSV_PATH_NAME=module.RAW_CSV_PATH_NAME,  RAW_ZIP_PATH_NAME=module.RAW_ZIP_PATH_NAME,
        SQLITE_DATA_PATH_NAME=module.SQLITE_DATA_PATH_NAME)
    CONFIG.SERVER = EasyDict(PORTS=module.PORTS)


def setup_logger():
    handlers = [logging.StreamHandler()]
    log_path = os.path.dirname(CONFIG.LOGGING.LOG_FILE_LOC)
    err = None
    if not os.path.isdir(log_path):
        try:
            os.makedirs(log_path, exist_ok=True)
        except Exception as e:
            err = e
        finally:
            if os.path.isdir(log_path):
                handlers.append(
                    TimedRotatingFileHandler(CONFIG.LOGGING.LOG_FILE_LOC, when='midnight', backupCount=7))

    logging.basicConfig(level=CONFIG.LOGGING.LOG_LEVEL, format=CONFIG.LOGGING.LOG_FORMAT, handlers=handlers)
    if len(handlers) == 1:
        logging.error(f'Cannot create file logger {CONFIG.LOGGING.LOG_FILE_LOC} with error: {err}')


def _display_path(args: argparse.Namespace):
    """
    ---
    Default config:
    Argument specified config:
    ---
    Default raw csv data:
    Configure specified raw csv data:
    Argument specified raw csv data:
    ---
    Default raw zip data:
    Configure specified raw zip data:
    Argument specified raw zip data:
    ---
    Default log path:
    Configure specified log path:
    ---
    Default SQLite db:
    Configure specified SQLite db:
    ---
    """
    # noinspection PyPep8Naming
    NOT_SPECIFIED = 'Not specified'

    d_config = default_config.__file__
    as_config = NOT_SPECIFIED if args.config == d_config else args.config

    d_raw_csv = default_config.RAW_CSV_PATH_NAME
    cs_raw_csv = NOT_SPECIFIED if as_config == NOT_SPECIFIED else CONFIG.PATH.RAW_DATA_PATH_NAME
    as_raw_csv = NOT_SPECIFIED if args.csv is None else args.csv

    d_raw_zip = default_config.RAW_ZIP_PATH_NAME
    cs_raw_zip = NOT_SPECIFIED if as_config == NOT_SPECIFIED else CONFIG.PATH.RAW_ZIP_PATH_NAME
    as_raw_zip = NOT_SPECIFIED if args.zip is None else args.zip

    d_log = default_config.LOG_FILE_PATH
    cs_log = NOT_SPECIFIED if as_config == NOT_SPECIFIED else CONFIG.LOGGING.LOG_FILE_LOC

    d_sqlite = default_config.SQLITE_DATA_PATH_NAME
    cs_sqlite = NOT_SPECIFIED if as_config == NOT_SPECIFIED else CONFIG.PATH.SQLITE_DATA_PATH_NAME

    max_length = max(
        len(d_config), len(as_config), len(d_raw_csv), len(cs_raw_csv), len(as_raw_csv),
        len(d_log), len(cs_log), len(d_sqlite), len(cs_sqlite)
    )

    showpath_template = '| {{:<35}} | {{:<{max_length}}} |'.format(max_length=max_length // 5 * 5 + 5)
    separator = '-' * len(showpath_template.format('', ''))
    path_list = [
        '', separator,
        showpath_template.format('Default config', d_config),
        showpath_template.format('Argument specified config', as_config),
        separator,
        showpath_template.format('Default raw csv data', d_raw_csv),
        showpath_template.format('Configure specified raw csv data', cs_raw_csv),
        showpath_template.format('Argument specified raw csv data', as_raw_csv),
        separator,
        showpath_template.format('Default raw zip data', d_raw_zip),
        showpath_template.format('Configure specified raw zip data', cs_raw_zip),
        showpath_template.format('Argument specified raw zip data', as_raw_zip),
        separator,
        showpath_template.format('Default log path', d_log),
        showpath_template.format('Configure specified log path', cs_log),
        separator,
        showpath_template.format('Default SQLite db', d_sqlite),
        showpath_template.format('Configure specified SQLite db', cs_sqlite),
        separator, ''
    ]
    logging.info('\n'.join(path_list))


def display_path(args: argparse.Namespace):
    art = text2art('IP2LOC', font='epic')
    logging.info(f'\n{art}')

    if args.showpath:
        _display_path(args)
    else:  # path abbr
        logging.info(f'CONFIGURE FILE: {args.config}')
        logging.info(f'LOG FILE: {CONFIG.LOGGING.LOG_FILE_LOC}')


def adjust_arguments(args: argparse.Namespace):

    if not args.showpath and not args.loaddata and not args.runserver:
        # no action specified, run the server as default
        args.runserver = True

    if not os.path.exists(CONFIG.PATH.SQLITE_DATA_PATH_NAME) or \
            not os.path.isfile(CONFIG.PATH.SQLITE_DATA_PATH_NAME) or \
            not os.path.getsize(CONFIG.PATH.SQLITE_DATA_PATH_NAME) > 0:
        # no sqlite data found
        logging.warning('No SQLite db found, load data first!')
        args.loaddata = True


def entry():
    args = parse_args()
    load_config(config_path_name=args.config)
    setup_logger()
    display_path(args)
    if args.showpath and not args.loaddata and not args.runserver:
        # only showpath
        exit(0)
    adjust_arguments(args)

    if args.loaddata:
        csv_path_name = args.csv or CONFIG.PATH.RAW_CSV_PATH_NAME
        zip_path_name = args.zip or CONFIG.PATH.RAW_ZIP_PATH_NAME
        unzip = False
        if csv_path_name and os.path.exists(csv_path_name) and os.path.getsize(csv_path_name) > 0:
            # csv file is available
            logging.info(f"Load data: \n"
                         f"\tfrom '{csv_path_name}' \n"
                         f"\tto '{CONFIG.PATH.SQLITE_DATA_PATH_NAME}' \n"
                         f"\tdata version: {args.dataver if args.dataver else 'Not specified'}")
        elif zip_path_name and os.path.exists(zip_path_name) and os.path.getsize(zip_path_name) > 0:
            # csv file is not available but zip file is
            logging.info(f"Load data: \n"
                         f"\tfrom '{zip_path_name}' \n"
                         f"\tto '{CONFIG.PATH.SQLITE_DATA_PATH_NAME}' \n"
                         f"\tdata version: {args.dataver if args.dataver else 'Not specified'}")
            unzip = True
        else:
            logging.fatal('Neither CSV nor ZIP file is available for data loading.')
            logging.info("See 'Track the Latest Data' in README for where to download the data and how to load.")
            exit(1)

        load_data(
            csv_path_name=csv_path_name, zip_path_name=zip_path_name, unzip=unzip,
            sqlite_path_name=CONFIG.PATH.SQLITE_DATA_PATH_NAME, specified_version=args.dataver)

    if args.runserver:
        check_data_version()
        runserver(sqlite_path_name=CONFIG.PATH.SQLITE_DATA_PATH_NAME, ports=CONFIG.SERVER.PORTS)

