#!/usr/bin/env python
import argparse
import logging
import sys

from comet_ml.offline import main_upload

LOGGER = logging.getLogger("comet_ml")


def main():
    # Called via `comet-upload EXP.zip`
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "archives", nargs="+", help="the offline experiment archives to upload"
    )
    parser.add_argument(
        "--force-reupload",
        help="force reupload offline experiments that were already uploaded",
        action="store_const",
        const=True,
        default=False,
    )

    parsed_args = parser.parse_args(sys.argv[1:])

    main_upload(parsed_args.archives, parsed_args.force_reupload)


if __name__ == "__main__":
    # Called via `python -m comet_ml.scripts.comet_upload EXP.zip`
    main()
