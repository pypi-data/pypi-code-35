'''
Command line interfaces for importreqs.
'''
import argparse
from . import importreqs

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", default="",
                        help="Python command line for loading dependencies.")
    return parser.parse_args()


def main():
    args = vars(parse_args())
    if args.get('command'):
        print(importreqs.generate_reqs_for_command(args['command']))


if __name__ == '__main__':
    main()
