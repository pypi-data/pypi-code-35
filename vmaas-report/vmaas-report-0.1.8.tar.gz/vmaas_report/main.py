#!/usr/bin/env python
import argparse

from vmaas_report.evaluator import Evaluator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--status", action="store_true", help="show status of configured VMaaS server")
    parser.add_argument("-r", "--request", action="store_true", help="print prepared VMaaS request and finish")
    args = parser.parse_args()

    evaluator = Evaluator()

    if args.status:
        evaluator.print_status()
    elif args.request:
        evaluator.print_request()
    else:
        evaluator.evaluate_updates()

if __name__ == "__main__":
    main()
