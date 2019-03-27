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

to_account = '0x79BB4B36F9bBa2165690790793eB3CAE8045856d'

tx = Helper.send_eth(skale, to_account, 10000, wallet)
receipt = Helper.await_receipt(skale.web3, tx)

balance = skale.web3.eth.getBalance(to_account)
print(f'Account balance: {balance}')
