import os
import json
from web3 import Web3
import sys, logging
from logging import Formatter, StreamHandler

from examples.schains.automation.config import WALLETS_FILE


def init_default_logger():
    handlers = []
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    handlers.append(stream_handler)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers)


def get_wallets():
    with open(WALLETS_FILE) as f:
        return json.load(f)


class safelist(list):
    def get(self, index, default=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            return default
