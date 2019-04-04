import argparse
from jovian_data.utils.datasets import (create_dataset, list_datasets,
                                        mount_dataset, generate_dataset, list_cache)
from jovian_data._version import __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('arg1', nargs='?')
    parser.add_argument('arg2', nargs='?')

    args = parser.parse_args()
    command = args.command
    if command == 'version':
        print('Jovian-data library version: ' + __version__)
    elif command == 'list':
        list_datasets()
    elif command == 'list_cache' or command == 'lc':
        list_cache()
    elif command == 'create':
        if not args.arg1:
            print('Please provide folder name to create dataset')
            return
        create_dataset(args.arg1)
    elif command == 'mount':
        if not args.arg1:
            print('Please provide dataset name to mount')
            return
        mount_dataset(args.arg1, args.arg2)
    elif command == 'cache':
        if not args.arg1:
            print('Please provide dataset name and version to generate')
            return
        generate_dataset(args.arg1)
    else:
        print(command, "command not found")


if __name__ == '__main__':
    main()
