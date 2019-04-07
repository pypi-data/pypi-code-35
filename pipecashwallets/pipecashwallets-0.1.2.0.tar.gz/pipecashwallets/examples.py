import logging


class ExampleMinimalWallet:

    def start(self, log):
        '''Help:
        log debug => log.debug("some string")
        log info => log.info("some string")
        log warning => log.warn("some string")
        log error => log.error("some string")'''
        pass

    def checkBalance(self):
        '''Returns the available funds in the wallet'''
        pass

    def send(self, amount, address):
        '''Sends funds to the specified address'''
        pass

    def getReceiveAddress(self):
        '''Returns a public receiving address of this wallet'''
        pass

    def getLatestTransactions(self, numOfTransactions=10, transactionsToSkip=0):
        '''Returns a list containing the latest transactions of this wallet.
        Transactions are ordered by their recency (newest first, oldest last)
        'numOfTransactions' is the maximum number of transactions to return
        'transactionsToSkip' specifies how many (newer) transactions to skip, before getting the older ones

        Each transaction should be represented as a 'dict' like:
        
        {
            'amount': Decimal = the total sum of money transfered in this TX (a positive number)
            'time': int = epoch timestamp in seconds
            'id': string = the transaction id
            'confirmations': int = how many blocks confirm the transaction.
        }

        Different wallets can add additional values in the dictionary, but the listed ones are mandatory.'''
        pass


class ExampleWallet:

    def start(self, log):
        '''Help:
        log debug => log.debug("some string")
        log info => log.info("some string")
        log warning => log.warn("some string")
        log error => log.error("some string")'''
        pass

    def __init__(self):

        self.options = {}
        # the options field will be populated
        #   with options from the scenario file,
        #   or with the default options.

        self.description = ""
        # Describes how the wallet works and how to configure the options.
        # Markdown is permitted.

        self.default_options = {}
        # in case no options are provided in the scenario,
        # these default options will be used.

        self.uses_secret_variables = []
        # list of secrets variable names
        #   used to get access to sensitive data
        #   that can't be included in the scenario or options.
        #   Example - wallet private keys

        self.secrets = {}
        # will be populated with variables requested in uses_secret_variables

    def validate_options(self):
        '''Called once, before the wallet is started.
        Should raise an exception if provided options are invalid'''
        pass

    def check_dependencies_missing(self):
        '''Called once, before the wallet is started.
        Should raise an exception if wallet dependencies are missing'''
        pass

    def checkBalance(self):
        '''Returns the available funds in the wallet'''
        pass

    def send(self, amount, address):
        '''Sends funds to the specified address'''
        pass

    def getReceiveAddress(self):
        '''Returns a public receiving address of this wallet'''
        pass

    def getLatestTransactions(self, numOfTransactions=10, transactionsToSkip=0):
        '''Returns a list containing the latest transactions of this wallet.
        Transactions are ordered by their recency (newest first, oldest last)
        'numOfTransactions' is the maximum number of transactions to return
        'transactionsToSkip' specifies how many (newer) transactions to skip, before getting the older ones

        Each transaction should be represented as a 'dict' like:

        {
            'amount': Decimal = the total sum of money transfered in this TX (a positive number)
            'time': int = epoch timestamp in seconds
            'id': string = the transaction id
            'confirmations': int = how many blocks confirm the transaction.
        }

        Different wallets can add additional values in the dictionary, but the listed ones are mandatory.'''
        pass
