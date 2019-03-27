import argparse
import os
import sys

from mungo.base import create_environment, install_packages, read_environment_description, _get_condarc_channels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jobs", type=int, help="number of jobs", default=4)

    subparsers = parser.add_subparsers(title='subcommands',
                                       dest='command',
                                       description='valid subcommands',
                                       help='additional help')
    subparsers.required = True

    parser_create = subparsers.add_parser('create')
    parser_create.add_argument("-n", "--name", help="the name of the environment")
    parser_create.add_argument("package_spec", nargs="*")
    parser_create.add_argument("--file", metavar="FILE", default=None)
    parser_create.add_argument("--channel", "-c", nargs=1, action="append", metavar="CHANNEL", default=[])
    parser_create.add_argument("--dag", action="store_true", default=False, help="Do not execute anything and print "
                                                                                 "the directed acyclic graph of "
                                                                                 "package dependency in the dot "
                                                                                 "language. Recommended use on Unix "
                                                                                 "systems: mungo create --dag | dot | "
                                                                                 "display")
    parser_create.add_argument("-y", "--yes", help="Do not ask for confirmation.", action="store_true")

    parser_install = subparsers.add_parser('install')
    parser_install.add_argument("-n", "--name", help="the name of the environment", default=None)
    parser_install.add_argument("package_spec", nargs="+")
    parser_install.add_argument("--file", metavar="FILE", default=None)
    parser_install.add_argument("--channel", "-c", nargs=1, action="append", metavar="CHANNEL", default=[])
    parser_install.add_argument("--dag", action="store_true", default=False, help="Do not execute anything and print "
                                                                                  "the directed acyclic graph of "
                                                                                  "package dependency in the dot "
                                                                                  "language. Recommended use on Unix "
                                                                                  "systems: mungo create --dag | dot "
                                                                                  "| display")
    parser_install.add_argument("-y", "--yes", help="Do not ask for confirmation.", action="store_true")

    args = parser.parse_args()
    # use either the supplied name, the current prefix or the default env 'base' in that order
    args.name = args.name or os.getenv('CONDA_DEFAULT_ENV', default='base')
    jobs = args.jobs
    command = args.command
    dag = args.dag
    ask_for_confirmation = not args.yes

    channels = [channel for channel in args.channel]
    packages = set(args.package_spec)
    if args.file is not None:
        name, channels_rc, packages_rc, pip = read_environment_description(args.file)
        name = name or args.name  # if the environment description does not supply a name, use args.name instead
        channels.extend(channels_rc)
        packages |= set(packages_rc)
    else:
        name = args.name
        pip = []

    default_channels = _get_condarc_channels()
    channels.extend(default_channels)

    print("WARNING: mungo is still in alpha, use at your own risk.", file=sys.stderr)
    if command == "create":
        create_environment(name, channels, packages, pip, jobs, dag, ask_for_confirmation)
    elif command == "install":
        install_packages(name, channels, packages, pip, jobs, dag, ask_for_confirmation)
