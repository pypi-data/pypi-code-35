#!/usr/bin/env python
import argparse
import os
import sys

from vmaas_report.evaluator import Evaluator


def validate_args(args):
    errors = 0
    if args.file:
        if not os.path.isfile(args.file) and not args.file == "-":
            print("ERROR: File doesn't exist - \"%s\"." % args.file)
            errors += 1
    return errors == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--status", action="store_true",
                        help="show status of configured VMaaS server")
    parser.add_argument("-r", "--request", action="store_true",
                        help="""print prepared VMaaS request of current system and finish""")
    parser.add_argument("-f", "--file", action="store",
                        help="""evaluate prepared VMaaS request from JSON file""")
    args = parser.parse_args()
    if not validate_args(args):
        print("ERROR: Argument validation failed, exiting.")
        sys.exit(1)

    evaluator = Evaluator()

    if args.status:
        evaluator.print_status()
    elif args.request:
        evaluator.print_request()
    else:
        evaluator.evaluate_updates(request_file=args.file)

    if evaluator.errors:
        sys.exit(2)

if __name__ == "__main__":
    main()
