#TODO: implement wallet

import logging

class BitcoinBTC_RPC:

    def __init__(self):

        self.description = ""
        self.options = {}
        self.default_options = { }

        self.uses_secret_variables = [
            "BTC_RPC_USER",
            "BTC_RPC_PASSWORD"
        ]

        self.secrets = {}


    def start(self, log):
        raise NotImplementedError()

    def validate_options(self):
        raise NotImplementedError()

    def check_dependencies_missing(self):
        from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

    def checkBalance(self):
        raise NotImplementedError()

    def send(self, amount, address):
        raise NotImplementedError()

    def getReceiveAddress(self):
        raise NotImplementedError()

    def getLatestTransactions(self, numOfTransactions=10, transactionsToSkip=0):
        raise NotImplementedError()