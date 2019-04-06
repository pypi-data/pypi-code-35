# -*- coding: utf-8 -*-

import importlib
import sys
import os
import termcolor
import traceback
import io
from contextlib import redirect_stdout

from argparse import ArgumentParser
from link_migration.framework.version import VERSION
from link_migration.framework.model import DiscoverMigrations
from link_migration.framework.views import TerminalMessages

sys.path.insert(0, os.getcwd())


def link_migration():

    parser = ArgumentParser(description="Parameters to migrate.")
    parser.add_argument(
        "-u", "--up",
        dest="up", default=False, action="store_true",
        help="Execute python methods to upgrade schema of system."
    )

    parser.add_argument(
        "-d", "--down",
        dest="down", default=False, action="store_true",
        help="Execute python methods to downgrade schema of system."
    )

    parser.add_argument(
        "--no-exec", "--dry-run",
        dest="execute", default=True, action="store_false",
        help="Dry run the migration to see what will be executed."
    )

    parser.add_argument(
        "-v", "--version",
        dest="version", default=False, action="store_true",
        help="Version of actual migration."
    )

    parser.add_argument(
        "--package-version",
        dest="package_version", default=False, action="store_true",
        help="Displays link_migration's version and exit."
    )

    parser.add_argument(
        "-t", "--to",
        dest="version_to", default=0,
        help="Migrate to specific version ."
    )

    parser.add_argument(
        "-c", "--config-file",
        dest="config", default="link_migration.example_migrations.conf",
        help="Specify a custom configuration file."
    )

    parser.add_argument(
        "-m", "--make-migration"
    )

    args = parser.parse_args()
    args.config = importlib.import_module(args.config)

    discovered_migrations = DiscoverMigrations(**vars(args))
    terminal_message = TerminalMessages(discovered_migrations, **vars(args))

    if args.package_version:
        print(f'Package Version: {termcolor.colored(VERSION, "blue")}', flush=True)

    if args.version:
        print(f'Current Migration Version: {terminal_message.current_version()}', flush=True)

    if (args.down and args.up) or (args.down and args.version_to) or (args.up and args.version_to):
        print(f'Cannot run migrations. Please specify only Up, Down, or To', flush=True)

    if args.down or args.up or args.version_to:
        migrate_type = {
            (True, False, False): discovered_migrations.upgrade,
            (False, True, False): discovered_migrations.downgrade,
            (False, False, True): discovered_migrations.specified
        }[(args.up, args.down, bool(args.version_to))]

        migrations_to_execute = list(discovered_migrations.migrations(migrate_type))
        migrate_type = discovered_migrations.upgrade if discovered_migrations.is_up() else discovered_migrations.downgrade

        if not migrations_to_execute:
            print(termcolor.colored(
                f'No migrations need to be executed, already at the correct version: {terminal_message.current_version()}',
                "green"
            ), flush=True)

        try:
            for migration in migrations_to_execute:
                terminal_message.make_message(migrate_type, migration)
                with io.StringIO() as buf, redirect_stdout(buf):
                    getattr(migration, migrate_type)()
                    output = buf.getvalue()
                terminal_message.print_message(output, 'magenta')
        except Exception as e:
            print(traceback.format_exc())
            terminal_message.error_message(migrate_type, migration, e)
            sys.exit()


if __name__ == '__main__':
    link_migration()
