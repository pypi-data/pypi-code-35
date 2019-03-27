
from web3 import Web3, WebsocketProvider, HTTPProvider


ip = "18.191.218.52"
port = 7003

web3 = Web3(HTTPProvider(f'http://{ip}:{port}'))

#if not web3.eth.accounts:
#    web3.personal.importRawKey('3b403794d39dc13a41703f2cb6d6704119c7e38c024f97cce33db07eb4afe671', '11111111')
owner = web3.eth.accounts[0]
web3.personal.unlockAccount(owner, '11111111')
print("Unlocked")