import os
from cement.utils import fs
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
import sqlite3

from benchgrape.config import DB_FILE
from benchgrape.controllers.benchmark import Benchmark
from benchgrape.controllers.test_data import TestData
from benchgrape.controllers.websocket_stability import Stability
from benchgrape.core.db import Mapper
from .core.exc import BenchGrapeError
from .controllers.base import Base

# configuration defaults
CONFIG = init_defaults('benchgrape')
CONFIG['benchgrape']['db_file'] = DB_FILE


def extend_sqlite(app):
    app.log.info('initializing sqlite')
    db_file = app.config.get('benchgrape', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.info('sqlite database file is: %s' % db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    db_conn = sqlite3.connect(db_file, isolation_level='EXCLUSIVE')
    app.extend('db', db_conn)


def migrate(app):
    for klass in inheritors(Mapper):
        klass(app.db, app.log).init_db()


class BenchGrape(App):
    """Bench Grape primary application."""

    class Meta:
        label = 'benchgrape'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            TestData,
            Stability,
            Benchmark,
        ]

        hooks = [
            ('post_setup', extend_sqlite),
            ('post_setup', migrate),
        ]


class BenchGrapeTest(TestApp,BenchGrape):
    """A sub-class of BenchGrape that is better suited for testing."""

    class Meta:
        label = 'benchgrape'


def main():
    with BenchGrape() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except BenchGrapeError as e:
            print('BenchGrapeError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


if __name__ == '__main__':
    main()
