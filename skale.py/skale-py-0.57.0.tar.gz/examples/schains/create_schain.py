import string
import random
from skale import Skale, BlockchainEnv
import skale.utils.helper as Helper

from web3 import Web3

import os, sys, logging
from logging import Formatter, StreamHandler

handlers = []
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
handlers.append(stream_handler)

logging.basicConfig(level=logging.DEBUG, handlers=handlers)

skale = Skale(BlockchainEnv.TEST)


addr = '0x5112cE768917E907191557D7E9521c2590Cdd3A0'
address_fx = Web3.toChecksumAddress(addr)
wallet = {
    'address': address_fx,
    'private_key': os.environ['ETH_PRIVATE_KEY']
}

def generate_random_name(len=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=len))

def create_schain():

    lifetime_years = 1
    lifetime_seconds = lifetime_years * 366 * 86400
    type_of_nodes = 4

    price_in_wei = skale.schains.get_schain_price(type_of_nodes, lifetime_seconds)

    #name = generate_random_name()
    name = 'test_schain'

    res = skale.manager.create_schain(lifetime_seconds, type_of_nodes, price_in_wei, name, wallet)
    receipt = Helper.await_receipt(skale.web3, res['tx'])
    return receipt

if __name__ == "__main__":
    res = create_schain()
    print(res)