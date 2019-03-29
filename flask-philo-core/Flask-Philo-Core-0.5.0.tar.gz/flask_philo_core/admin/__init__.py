from .project import start_project

import argparse


def main():
    cmd = {
        'startproject': start_project
    }
    parser = argparse.ArgumentParser(
        description='Admin tool for Flask-Philo projects')
    parser.add_argument('command', help='command to be executed')
    args, extra_params = parser.parse_known_args()

    if args.command not in cmd:
        print('Invalid command. Valid commands are:')

        for k in cmd.keys():
            print('\n * {}'.format(k))

        exit(1)

    cmd[args.command]()


if __name__ == '__main__':
    main()
