import os
from skale import Skale, BlockchainEnv
import skale.utils.helper as Helper

from web3 import Web3

skale = Skale(BlockchainEnv.AWS)

addr = '0x6870EA70c8582A3C3c778ae719b502e4644fD9dE'
address_fx = Web3.toChecksumAddress(addr)
wallet = {
    'address': address_fx,
    'private_key': os.environ['ETH_PRIVATE_KEY']
}

to_account = '0xe35B0c45B445b4120C77c8F2eb33D025ABc04266'


res = skale.token.transfer(to_account, 100, wallet)
receipt = Helper.await_receipt(skale.web3, res['tx'])
print(receipt)
