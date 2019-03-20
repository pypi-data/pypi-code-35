from argparse import ArgumentParser

from .install import install, uninstall
from .read_changes import read_changes


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    install_parser = subparsers.add_parser("install")
    install_parser.set_defaults(handler=install)

    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.set_defaults(handler=uninstall)

    changes_parser = subparsers.add_parser("changes")
    changes_parser.set_defaults(handler=read_changes)

    args = parser.parse_args()
    args.handler()


if __name__ == "__main__":
    main()
