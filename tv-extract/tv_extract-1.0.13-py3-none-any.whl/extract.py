#! /usr/bin/env python3
import logging
import os
import sys

import multiprocessing_logging

from tv_extract.git_extract import git_extract

from pathlib import Path


from tv_extract.util import cli
from tv_extract.data import Config

def extract():
    _extract(cli.get_cli())

def _extract(config: Config) -> None:
    cache_root_dir = Path.home() / '.local' / 'share' / 'cache'
    cache_root_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=config.logging, format='%(message)s')
    multiprocessing_logging.install_mp_handler()
    try:
        os.makedirs(config.output_path)
    except OSError:
        pass
    if not os.path.isdir(config.output_path):
        logging.fatal('Output path is not a directory or does not exist')
        sys.exit(1)

    logging.info(f'Extract being written to: {config.output_path}')

    git_extract(config, cache_root_dir)

    # TODO: other extractors would be added here

if __name__ == '__main__': # pragma: no cover
    extract()
    sys.exit(0)
