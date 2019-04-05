#!/usr/bin/env python3
"""Check the status of some website."""

import argparse
import asyncio

import onweb

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument("websites", nargs="+", help="a list of online website")
PARSER.add_argument("-r", "--redirect", action="store_true", help="handle 3XX")


def main(argv=None):
    """Entry point of the script."""
    args = PARSER.parse_args(argv)
    loop = asyncio.get_event_loop()

    tasks = onweb.checkall(args.websites, redirect=args.redirect)

    for response in loop.run_until_complete(tasks):
        print(f"{response.status}\t{response.url}")


if __name__ == "__main__":
    main()
