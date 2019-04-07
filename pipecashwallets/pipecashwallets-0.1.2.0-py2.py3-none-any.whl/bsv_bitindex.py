# TODO: implement wallet

import logging
import requests
import json


class BitcoinSV_BitIndex:

    __baseURL = "https://api.bitindex.network/"

    __xpub_statusURL = __baseURL + "api/v2/xpub/status"
    __xpub_registerURL = __baseURL + "api/v2/xpub/register"
    __xpub_nextAddressURL = __baseURL + "api/v2/xpub/addrs/next"
    __xpub_balanceURL = __baseURL + "api/v2/xpub/balance"
    __xpub_txHistoryURL = __baseURL + "api/v2/xpub/txs"

    __addr_balanceURL = __baseURL + "api/v2/addrs/balance"
    __addr_txHistoryURL = __baseURL + "api/v2/addrs/txs"

    __tx_txDataURL = __baseURL + "api/v2/tx/"

    description = '''A wallet that uses the bitIndex API
    https://www.bitindex.network/

    Pass the key for the wallet in the secret variables.
    The key can be a:
    - public key (read only)
    - (not supported yet) private key
    - (not supported yet) xpub (read only)
    - (not supported yet) set of mnemonics
    - (not supported yet) xpriv
    '''

    def __init__(self):

        self.options = {}

        self.default_options = {
            "bitIndexApiKey": "8KSSwFpUXtCaesg9tKSdkxT1qb35Cw4Yjc5TpjX4YiBaTRPmApaW7xoYUQvhwFJBVM",
        }

        self.uses_secret_variables = ["BSV_BITINDEX_KEY"]
        self.secrets = {}

    def start(self, log):
        self.apiKey = self.options['bitIndexApiKey']

        key = self.secrets['BSV_BITINDEX_KEY']

        self.isPubKey = len(key) == 34
        self.isPrivKey = len(key) == 51
        self.isMnemonic12 = len(key.split(" ")) == 12
        self.isMnemonic24 = len(key.split(" ")) == 24
        self.isXpriv = len(key) == 111 and key.startswith("xprv")
        self.isXpub = len(key) == 111 and key.startswith("xpub")

        if self.isPubKey:
            self.address = key
        elif self.isPrivKey:
            raise NotImplementedError(
                "BitcoinSV_BitIndex doesn't work with private keys yet")
        elif self.isMnemonic12 or self.isMnemonic24:
            raise NotImplementedError(
                "BitcoinSV_BitIndex doesn't work with mnemonics yet")
        elif self.isXpriv:
            raise NotImplementedError(
                "BitcoinSV_BitIndex doesn't work with XPRIV yet")
        elif self.isXpub:
            self.xpub = key
            # TODO: call __registerURL and __statusURL to wait till the registration is done.
            raise NotImplementedError(
                "BitcoinSV_BitIndex doesn't work with XPUB yet")
        else:
            raise NotImplementedError(
                "The format of 'BSV_BITINDEX_KEY' was not recognized")

    def validate_options(self):
        pass

    def check_dependencies_missing(self):
        pass

    def checkBalance(self):
        if self.isPrivKey or self.isPubKey:
            r = requests.get(self.__addr_balanceURL, {
                'address': self.address,
                # 'api_key': self.apiKey
            })
            return json.loads(r.text)["data"][0]["confirmed"] / 100000000.0

        elif self.isMnemonic12 or self.isMnemonic24 or self.isXpriv or self.isXpub:
            r = requests.get(self.__xpub_balanceURL, {
                'xpub': self.xpub,
                'api_key': self.apiKey
            })
            raise NotImplementedError()

    def send(self, amount, address):
        if self.isPubKey or self.isXpub:
            raise AssertionError("Can not use 'send' in watch-only mode")
        elif self.isPrivKey:
            raise NotImplementedError()
        elif self.isMnemonic12 or self.isMnemonic24 or self.isXpriv:
            raise NotImplementedError()

    def getReceiveAddress(self):
        if self.isPrivKey or self.isPubKey:
            return self.address
        elif self.isMnemonic12 or self.isMnemonic24 or self.isXpriv or self.isXpub:
            r = requests.get(self.__xpub_nextAddressURL, {
                'xpub': self.xpub,
                'api_key': self.apiKey
            })
            print(r.url)
            print(r.text)

    def getLatestTransactions(self, numOfTransactions=10, transactionsToSkip=0):
        start = transactionsToSkip
        end = start + numOfTransactions

        if self.isPrivKey or self.isPubKey:
            r = requests.get(self.__addr_txHistoryURL, {
                'address': self.address,
                'api_key': self.apiKey
            })

            txList = json.loads(r.text)["data"]
            txList = [txList[i]
                      for i in range(start, end) if i > 0 and i < len(txList)]
            raise NotImplementedError()
        elif self.isMnemonic12 or self.isMnemonic24 or self.isXpriv or self.isXpub:
            r = requests.get(self.__xpub_txHistoryURL, {
                'xpub': self.xpub,
                'api_key': self.apiKey
            })
            raise NotImplementedError()
